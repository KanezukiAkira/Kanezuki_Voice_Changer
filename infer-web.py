# infer-web.py - Wrapper script to inject missing globals into the compiled backend
# This script defines functions that are expected by infer-web.pyc (the compiled real backend)
# but were not compiled into it due to compilation environment differences.

import os
import sys
import shutil

# --- AUTO CLEANUP LEGACY/JUNK FILES ---
try:
    _junk = ["go-web.bat", "go-web-release.bat", "test.py", "build_release.py", "build_release.pyc", "launcher.py"]
    for _j in _junk:
        if os.path.exists(_j):
            os.remove(_j)
            
    _locale_dir = os.path.join("i18n", "locale")
    if os.path.exists(_locale_dir):
        for _f in os.listdir(_locale_dir):
            if _f.endswith(".json") and _f not in ["vi_VN.json", "en_US.json"]:
                os.remove(os.path.join(_locale_dir, _f))
                
    _docs_dir = "docs"
    if os.path.exists(_docs_dir):
        _doc_junks = ["cn", "fr", "jp", "kr", "tr", "小白简易教程.doc"]
        for _d in _doc_junks:
            _p = os.path.join(_docs_dir, _d)
            if os.path.exists(_p):
                if os.path.isdir(_p):
                    shutil.rmtree(_p)
                else:
                    os.remove(_p)
except:
    pass
# --------------------------------------

import builtins
import zipfile
import shutil
import requests

# ─────────────────────────────────────────────────────────────────────────────
# Helper: scan_models
# Returns a dict mapping display_name -> (pth_path, index_path)
# ─────────────────────────────────────────────────────────────────────────────
def scan_models():
    from dotenv import load_dotenv
    load_dotenv()
    weight_root = os.getenv("weight_root", "assets/weights")
    index_root  = os.getenv("index_root",  "logs")

    # Collect all index files
    index_files = []
    if os.path.isdir(index_root):
        for r, _, files in os.walk(index_root):
            for f in files:
                if f.endswith(".index") and "trained" not in f:
                    index_files.append(os.path.join(r, f))

    models = {}
    if not os.path.isdir(weight_root):
        return models

    for fname in os.listdir(weight_root):
        if not fname.endswith(".pth"):
            continue
        display_name = os.path.splitext(fname)[0]
        pth_path     = os.path.join(weight_root, fname)

        # Try to find matching index
        idx_path = ""
        for idx in index_files:
            basename = os.path.basename(idx)
            if display_name in basename:
                idx_path = idx
                break
        # Fuzzy match
        if not idx_path:
            parts = display_name.split("_")
            while len(parts) > 1 and not idx_path:
                parts.pop()
                prefix = "_".join(parts)
                for idx in index_files:
                    if prefix in os.path.basename(idx):
                        idx_path = idx
                        break

        models[display_name] = (pth_path, idx_path)

    return models


# ─────────────────────────────────────────────────────────────────────────────
# Helper: GradioFileMock
# ─────────────────────────────────────────────────────────────────────────────
class GradioFileMock:
    def __init__(self, name: str):
        self.name = name
        self.file = open(name, "rb")

    def close(self):
        if self.file and not self.file.closed:
            self.file.close()

    def __del__(self):
        self.close()


# ─────────────────────────────────────────────────────────────────────────────
# Helper: import_model_zip
# ─────────────────────────────────────────────────────────────────────────────
def import_model_zip(file_obj):
    from dotenv import load_dotenv
    load_dotenv()

    weight_root = os.getenv("weight_root", "assets/weights")
    index_root  = os.getenv("index_root",  "logs")
    os.makedirs(weight_root, exist_ok=True)
    os.makedirs(index_root,  exist_ok=True)

    zip_path = file_obj.name if hasattr(file_obj, "name") else str(file_obj)

    if not os.path.exists(zip_path):
        return "Không tìm thấy file ZIP: " + zip_path, {"value": "", "__type__": "update"}

    if not zipfile.is_zipfile(zip_path):
        return "File không phải định dạng ZIP hợp lệ.", {"value": "", "__type__": "update"}

    imported_pth   = []
    imported_index = []

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                basename = os.path.basename(member)
                if not basename:
                    continue

                if basename.endswith(".pth"):
                    dest = os.path.join(weight_root, basename)
                    with zf.open(member) as src, open(dest, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    imported_pth.append(basename)

                elif basename.endswith(".index") and "trained" not in basename:
                    dest = os.path.join(index_root, basename)
                    with zf.open(member) as src, open(dest, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    imported_index.append(basename)

    except Exception as e:
        import traceback
        return "Lỗi giải nén ZIP: " + traceback.format_exc(), {"value": "", "__type__": "update"}

    if not imported_pth and not imported_index:
        return (
            "ZIP không chứa file .pth hoặc .index nào hợp lệ.",
            {"value": "", "__type__": "update"},
        )

    parts = []
    if imported_pth:
        parts.append("Mô hình: " + ", ".join(imported_pth))
    if imported_index:
        parts.append("Index: " + ", ".join(imported_index))
    status = "Thành công! Đã nhập: " + " | ".join(parts)

    first_model = os.path.splitext(imported_pth[0])[0] if imported_pth else ""
    return status, {"value": first_model, "__type__": "update"}


# ─────────────────────────────────────────────────────────────────────────────
# Helper: vc_single_local
# Called by the compiled backend with 17 positional args:
#   (sid=0, model_name_hint='', input_audio_path, is_uvr, uvr_model,
#    vocal_volume, beat_volume, f0_up_key, f0_file, f0_method,
#    file_index1='', file_index, index_rate, filter_radius=3,
#    resample_sr=0, rms_mix_rate=0.25, protect)
# ─────────────────────────────────────────────────────────────────────────────
def vc_single_local(
    sid,
    model_name_hint,   # arg2: usually '' passed by compiled backend
    input_audio_path,
    is_uvr,
    uvr_model,
    vocal_volume,
    beat_volume,
    f0_up_key,
    f0_file,
    f0_method,
    file_index1,       # arg11: extra index path, often ''
    file_index,
    index_rate,
    filter_radius,
    resample_sr,
    rms_mix_rate,
    protect,
):
    try:
        from dotenv import load_dotenv
        load_dotenv()

        # The real pyc ALREADY calls vc.get_vc(rel_pth) in the convert endpoint
        # BEFORE calling vc_single_local. So by the time we run, the vc object
        # in _globals already has pipeline set.
        # We store _globals in builtins._rvc_exec_globals after exec() so we can
        # access the live vc object here.

        _exec_globals = getattr(builtins, '_rvc_exec_globals', None)

        if isinstance(sid, str) and sid:
            # Load model from name (rare: sid is usually 0)
            from infer.modules.vc.modules import VC
            from configs.config import Config
            config = Config()
            vc_obj = VC(config)
            models  = scan_models()
            rel_pth = ""
            display = sid.replace(".pth", "")
            if display in models:
                pth_path, idx_path = models[display]
                weight_root = os.getenv("weight_root", "assets/weights")
                rel_pth = pth_path
                if pth_path.startswith(weight_root):
                    rel_pth = pth_path[len(weight_root):].lstrip("/\\")
                if not file_index and idx_path:
                    file_index = idx_path
            vc_obj.get_vc(rel_pth)
        elif _exec_globals is not None and _exec_globals.get('vc') is not None:
            # Use the vc object from exec globals directly — the real pyc already
            # called vc.get_vc() so pipeline should be ready.
            vc_obj = _exec_globals['vc']
            # Verify pipeline is actually loaded
            if vc_obj.pipeline is None:
                # Pipeline not ready — force load using select_model's logic
                models = scan_models()
                if models:
                    first_name = next(iter(models))
                    pth_path, idx_path = models[first_name]
                    weight_root = os.getenv("weight_root", "assets/weights")
                    rel_pth = pth_path
                    if pth_path.startswith(weight_root):
                        rel_pth = pth_path[len(weight_root):].lstrip("/\\")
                    vc_obj.get_vc(rel_pth)
        else:
            # Last resort: create fresh VC and try to load first available model
            from infer.modules.vc.modules import VC
            from configs.config import Config
            config = Config()
            vc_obj = VC(config)
            models = scan_models()
            if models:
                first_name = next(iter(models))
                pth_path, idx_path = models[first_name]
                weight_root = os.getenv("weight_root", "assets/weights")
                rel_pth = pth_path
                if pth_path.startswith(weight_root):
                    rel_pth = pth_path[len(weight_root):].lstrip("/\\")
                vc_obj.get_vc(rel_pth)

        # Use file_index1 as fallback if file_index is empty
        effective_index = file_index if file_index else file_index1

        # Optional UVR separation
        actual_input = input_audio_path
        instrumental_path = None  # Track background music for mixing later
        if is_uvr:
            try:
                import sys as _sys
                from infer.modules.uvr5.modules import uvr as _uvr
                import tempfile, uuid as _uuid
                sep_dir = os.path.join(tempfile.gettempdir(), "rvc_uvr_" + _uuid.uuid4().hex)
                os.makedirs(sep_dir, exist_ok=True)

                _mock = GradioFileMock(input_audio_path)
                list(_uvr(uvr_model, "", sep_dir, [_mock], sep_dir, 10, "wav"))

                # Determine if vocal and instrument are swapped by the UVR model
                is_hp3 = "HP3" in uvr_model and "DeEcho" not in uvr_model

                vocal_file = None
                inst_file = None

                for f in os.listdir(sep_dir):
                    f_lower = f.lower()
                    full_path = os.path.join(sep_dir, f)
                    if not f_lower.endswith(('.wav', '.flac', '.mp3', '.ogg', '.m4a')):
                        continue
                    
                    is_vocal_named = "vocal" in f_lower
                    is_inst_named = "instrument" in f_lower or "accompan" in f_lower or "others" in f_lower

                    if is_hp3:
                        if is_vocal_named:
                            inst_file = full_path
                        elif is_inst_named:
                            vocal_file = full_path
                    else:
                        if is_vocal_named:
                            vocal_file = full_path
                        elif is_inst_named:
                            inst_file = full_path

                if vocal_file:
                    actual_input = vocal_file
                if inst_file:
                    instrumental_path = inst_file

                try:
                    print(f"[UVR Scanner] Model: {uvr_model}, is_hp3: {is_hp3} -> vocal: {actual_input}, instrumental: {instrumental_path}", file=_sys.stderr)
                except Exception:
                    pass
            except Exception as _uvr_err:
                import sys as _sys
                try:
                    print(f"[UVR Scanner Error] {_uvr_err}", file=_sys.stderr)
                except Exception:
                    pass
                pass  # Fall back to raw audio if UVR fails

        info, audio = vc_obj.vc_single(
            0,
            actual_input,
            int(f0_up_key),
            f0_file,
            f0_method,
            effective_index,
            effective_index,
            float(index_rate),
            int(filter_radius),
            int(resample_sr),
            float(rms_mix_rate),
            float(protect),
        )

        # ── Mix converted vocals with background music (UVR) ──────────────────
        if (
            is_uvr
            and instrumental_path
            and os.path.exists(instrumental_path)
            and audio is not None
            and audio[1] is not None
        ):
            try:
                import soundfile as _sf
                import numpy as _np
                import sys as _sys

                tgt_sr, vocal_arr = audio

                # Check the original dtype to see if it is an integer representation (like int16)
                is_int_type = _np.issubdtype(vocal_arr.dtype, _np.integer)

                # Ensure vocal is float32 mono 1D
                vocal_arr = _np.asarray(vocal_arr, dtype=_np.float32)
                if vocal_arr.ndim == 2:
                    vocal_arr = vocal_arr.mean(axis=1)

                # Convert vocal to float32 range [-1.0, 1.0] if it was integer
                if is_int_type:
                    vocal_arr = vocal_arr / 32768.0

                inst_arr, inst_sr = _sf.read(instrumental_path, always_2d=False)

                # Convert stereo instrumental to mono if needed
                inst_arr = _np.asarray(inst_arr, dtype=_np.float32)
                if inst_arr.ndim == 2:
                    inst_arr = inst_arr.mean(axis=1)

                # Convert instrumental to float32 range [-1.0, 1.0] if it is integer
                if _np.issubdtype(inst_arr.dtype, _np.integer):
                    inst_arr = inst_arr / 32768.0

                # Resample instrumental to match voice SR if different
                if inst_sr != tgt_sr:
                    import librosa as _librosa
                    inst_arr = _librosa.resample(
                        inst_arr, orig_sr=inst_sr, target_sr=tgt_sr
                    )

                # Apply dB volume settings (vocal_volume / beat_volume are in dB)
                try:
                    v_gain = float(10 ** (float(vocal_volume) / 20.0))
                    b_gain = float(10 ** (float(beat_volume) / 20.0))
                except Exception:
                    v_gain, b_gain = 1.0, 1.0

                # Trim to same length and mix
                min_len = min(len(vocal_arr), len(inst_arr))
                mixed = vocal_arr[:min_len] * v_gain + inst_arr[:min_len] * b_gain

                # Normalise to avoid clipping
                peak = float(_np.abs(mixed).max())
                if peak > 1.0:
                    mixed = mixed / peak

                # Convert mixed back to int16 to match original RVC output format
                mixed_int16 = (mixed * 32767.0).astype(_np.int16)

                audio = (tgt_sr, mixed_int16)
                info += "\n[UVR] Đã gộp nhạc nền."
                try:
                    print(f"[MIXING] OK - vocal {vocal_arr.shape} (int_type={is_int_type}) + inst {inst_arr.shape} -> mixed {mixed_int16.shape}", file=_sys.stderr)
                except Exception:
                    pass
            except Exception as _mix_err:
                import traceback as _mix_tb, sys as _sys2
                _err_detail = _mix_tb.format_exc()
                info += f"\n[UVR] Gộp nhạc nền thất bại: {_mix_err}"
                try:
                    print(f"[MIXING ERROR] {_err_detail}", file=_sys2.stderr)
                except Exception:
                    pass

        return info, audio

    except Exception:
        import traceback as _tb2
        return _tb2.format_exc(), (None, None)


# ─────────────────────────────────────────────────────────────────────────────
# Helper: vc_single_url
# Called by the compiled backend with 18 positional args:
#   (sid=0, url, is_uvr, uvr_model, vocal_volume, beat_volume,
#    f0_up_key, f0_file=None, f0_method, file_index1='', file_index,
#    index_rate, filter_radius=3, resample_sr=0, rms_mix_rate=0.25,
#    protect, cookies_str='Không dùng', _unused=None)
# ─────────────────────────────────────────────────────────────────────────────
def vc_single_url(
    sid,
    url,               # YouTube / TikTok / direct audio URL — arg2 (NO extra hint arg here)
    is_uvr,
    uvr_model,
    vocal_volume,
    beat_volume,
    f0_up_key,
    f0_file,
    f0_method,
    file_index1,       # arg10: extra empty string passed by compiled backend
    file_index,
    index_rate,
    filter_radius,
    resample_sr,
    rms_mix_rate,
    protect,
    cookies_str,
    _unused=None,
):
    import tempfile, uuid as _uuid

    try:
        tmp_dir  = tempfile.gettempdir()
        uid      = _uuid.uuid4().hex
        tmp_path = None

        # ── tikwm.com API: best for TikTok (no login needed) ─────────────────
        is_tiktok = "tiktok.com" in url.lower()
        if is_tiktok:
            try:
                api_resp = requests.get(
                    f"https://www.tikwm.com/api/?url={url}",
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=20,
                )
                api_data = api_resp.json()
                if api_data.get("code") == 0:
                    audio_url = (
                        api_data.get("data", {}).get("music")   # background music
                        or api_data.get("data", {}).get("play") # video audio track
                    )
                    if audio_url:
                        audio_resp = requests.get(
                            audio_url,
                            headers={"User-Agent": "Mozilla/5.0"},
                            timeout=60,
                            stream=True,
                        )
                        audio_resp.raise_for_status()
                        tmp_path = os.path.join(tmp_dir, f"rvc_tiktok_{uid}.mp3")
                        with open(tmp_path, "wb") as fout:
                            for chunk in audio_resp.iter_content(65536):
                                if chunk:
                                    fout.write(chunk)
            except Exception as _ttk_err:
                print(f"[TikTok API] Thử phương án dự phòng: {_ttk_err}", file=sys.stderr)

        # ── yt-dlp: handles YouTube, and non-TikTok sites ─────────────────────
        if not tmp_path or not os.path.exists(tmp_path):
            try:
                import yt_dlp as _ytdlp
                from yt_dlp.networking.impersonate import ImpersonateTarget

                out_tmpl = os.path.join(tmp_dir, f"rvc_ytdl_{uid}.%(ext)s")

                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": out_tmpl,
                    "quiet": True,
                    "no_warnings": True,
                    "noplaylist": True,
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "wav",
                    }],
                }

                # Use cookies file if it's a real path
                if (cookies_str and isinstance(cookies_str, str)
                        and os.path.isfile(cookies_str)):
                    ydl_opts["cookiefile"] = cookies_str

                # Try impersonation for better compatibility
                try:
                    ydl_opts["impersonate"] = ImpersonateTarget("chrome", None, "windows", None)
                except Exception:
                    pass

                with _ytdlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.extract_info(url, download=True)
                    candidate = os.path.join(tmp_dir, f"rvc_ytdl_{uid}.wav")
                    if not os.path.exists(candidate):
                        for f in os.listdir(tmp_dir):
                            if uid in f:
                                candidate = os.path.join(tmp_dir, f)
                                break
                    if os.path.exists(candidate):
                        tmp_path = candidate

            except Exception as _ydl_err:
                print(f"[yt-dlp] Không thể tải: {_ydl_err}", file=sys.stderr)

        # ── Fallback: plain HTTP for direct audio links ───────────────────────
        if not tmp_path or not os.path.exists(tmp_path):
            cookie_dict = {}
            if (cookies_str and isinstance(cookies_str, str)
                    and os.path.isfile(cookies_str)):
                with open(cookies_str, "r", encoding="utf-8", errors="ignore") as cf:
                    for line in cf:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        parts = line.split("\t")
                        if len(parts) >= 7:
                            cookie_dict[parts[5]] = parts[6]

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }

            resp = requests.get(
                url, headers=headers, cookies=cookie_dict,
                timeout=120, stream=True
            )
            resp.raise_for_status()

            ext = ".mp3"
            ct = resp.headers.get("Content-Type", "")
            if "wav" in ct:
                ext = ".wav"
            elif "ogg" in ct:
                ext = ".ogg"
            elif "flac" in ct:
                ext = ".flac"
            elif "mp4" in ct or "video" in ct:
                ext = ".mp4"

            tmp_path = os.path.join(tmp_dir, f"rvc_url_{uid}{ext}")
            with open(tmp_path, "wb") as fout:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        fout.write(chunk)


        if not tmp_path or not os.path.exists(tmp_path):
            return (
                "Không thể tải audio từ URL này. "
                "Hãy thử link trực tiếp hoặc kiểm tra lại URL.",
                (None, None)
            )

        result = vc_single_local(
            sid, "", tmp_path, is_uvr, uvr_model,
            vocal_volume, beat_volume,
            f0_up_key, f0_file, f0_method,
            file_index1, file_index, index_rate, filter_radius,
            resample_sr, rms_mix_rate, protect,
        )

        try:
            os.remove(tmp_path)
        except Exception:
            pass

        return result

    except Exception:
        import traceback as _tb
        return _tb.format_exc(), (None, None)


# ─────────────────────────────────────────────────────────────────────────────
# Inject all helpers into builtins so the compiled pyc can find them as globals
# ─────────────────────────────────────────────────────────────────────────────
builtins.scan_models       = scan_models
builtins.GradioFileMock    = GradioFileMock
builtins.import_model_zip  = import_model_zip
builtins.vc_single_local   = vc_single_local
builtins.vc_single_url     = vc_single_url

# ─────────────────────────────────────────────────────────────────────────────
# Execute the real compiled backend (renamed to infer-web-real.pyc)
# ─────────────────────────────────────────────────────────────────────────────
import marshal

_real_pyc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "infer-web-real.pyc")
if not os.path.exists(_real_pyc):
    raise FileNotFoundError(
        "infer-web-real.pyc not found! "
        "Please rename the original infer-web.pyc to infer-web-real.pyc first."
    )

with open(_real_pyc, "rb") as _f:
    _f.read(16)  # Skip 16-byte header (Python 3.7+)
    _code = marshal.load(_f)

_globals = {
    "__name__": "__main__",
    "__file__": _real_pyc,
    "__builtins__": builtins,
    # Pre-seed all injected helpers so they are available as module-level globals
    "scan_models":      scan_models,
    "GradioFileMock":   GradioFileMock,
    "import_model_zip": import_model_zip,
    "vc_single_local":  vc_single_local,
    "vc_single_url":    vc_single_url,
}

# ─────────────────────────────────────────────────────────────────────────────
# Post-exec helper: sync 'vc' object to builtins
# ─────────────────────────────────────────────────────────────────────────────
def _sync_vc_to_builtins():
    """Cache the global vc object into builtins after select_model."""
    _vc = _globals.get("vc", None)
    if _vc is not None:
        builtins._rvc_global_vc = _vc

# ─────────────────────────────────────────────────────────────────────────────
# Re-usable route hooking logic (handles both main process and worker imports)
# ─────────────────────────────────────────────────────────────────────────────
def _install_routes_and_hooks():
    try:
        _app = _globals.get("app", None)
        if _app is not None:
            try:
                if hasattr(_app, "blocks"):
                    # Find the FAQ tab and assign an elem_id
                    for comp in _app.blocks.blocks.values():
                        if type(comp).__name__ in ["TabItem", "Tab"]:
                            lbl = getattr(comp, "label", "") or ""
                            if "常见" in lbl or "FAQ" in lbl.upper() or "Hỏi đáp" in lbl or "Câu hỏi" in lbl:
                                comp.elem_id = "hide_faq_tab"
                                break
                    # Inject CSS to hide the tab button and content
                    css_to_add = "\n#hide_faq_tab-button { display: none !important; }\n#hide_faq_tab { display: none !important; }\n"
                    if getattr(_app.blocks, "css", None) is None:
                        _app.blocks.css = css_to_add
                    else:
                        _app.blocks.css += css_to_add
            except Exception as e:
                pass
            # 1. Install /api/select_model hook
            for _route in _app.routes:
                if hasattr(_route, "path") and _route.path == "/api/select_model":
                    if not getattr(_route.endpoint, "__wrapped_hook__", False):
                        _orig_endpoint = _route.endpoint

                        async def _wrapped_select_model(*args, **kwargs):
                            result = await _orig_endpoint(*args, **kwargs)
                            try:
                                _sync_vc_to_builtins()
                            except Exception as _sync_err:
                                print(f"[WRAPPER] Warning during VC sync: {_sync_err}", file=sys.stderr)
                            return result

                        _wrapped_select_model.__wrapped_hook__ = True
                        _route.endpoint = _wrapped_select_model
                        if hasattr(_route, "dependant") and _route.dependant is not None:
                            _route.dependant.call = _wrapped_select_model
                        from fastapi.routing import APIRoute
                        from starlette.routing import request_response
                        if isinstance(_route, APIRoute):
                            _route.app = request_response(_route.get_route_handler())
                        print("[WRAPPER] Hooked /api/select_model successfully.", file=sys.stderr)
                    break

            # 2. Install / route hook to serve frontend_extracted.html from disk
            for _route in _app.routes:
                if hasattr(_route, "path") and _route.path == "/":
                    if not getattr(_route.endpoint, "__wrapped_hook__", False):
                        _orig_index = _route.endpoint

                        async def _wrapped_index(*args, **kwargs):
                            from fastapi.responses import HTMLResponse
                            import sys, os
                            script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
                            html_path = os.path.join(script_dir, "frontend_extracted.html")
                            try:
                                with open(html_path, "r", encoding="utf-8") as fh:
                                    return HTMLResponse(content=fh.read())
                            except Exception as read_err:
                                try:
                                    with open(os.path.join(script_dir, "wrapper_error.log"), "a", encoding="utf-8") as lf:
                                        lf.write(f"Error reading {html_path}: {read_err}\n")
                                except: pass
                                import inspect
                                if inspect.iscoroutinefunction(_orig_index):
                                    res = await _orig_index(*args, **kwargs)
                                else:
                                    res = _orig_index(*args, **kwargs)
                                    if inspect.isawaitable(res):
                                        res = await res
                                
                                if hasattr(res, "body"):
                                    try:
                                        html = res.body.decode("utf-8")
                                        injection = """
                                        <script>
                                        setInterval(function() {
                                            try {
                                                var btns = document.querySelectorAll('button, div.tabitem, div[role="tab"]');
                                                for (var i = 0; i < btns.length; i++) {
                                                    var txt = btns[i].textContent || "";
                                                    if (txt.includes('FAQ') || txt.includes('Câu hỏi thường gặp')) {
                                                        btns[i].style.display = 'none';
                                                        var tabId = btns[i].getAttribute('aria-controls');
                                                        if (tabId) {
                                                            var tab = document.getElementById(tabId);
                                                            if (tab) tab.style.display = 'none';
                                                        }
                                                    }
                                                }
                                            } catch(e) {}
                                        }, 500);
                                        </script>
                                        """
                                        html = html.replace("</body>", injection + "</body>")
                                        from fastapi.responses import HTMLResponse
                                        return HTMLResponse(content=html, status_code=res.status_code, headers=dict(res.headers))
                                    except Exception as e:
                                        pass
                                return res

                        _wrapped_index.__wrapped_hook__ = True
                        _route.endpoint = _wrapped_index
                        if hasattr(_route, "dependant") and _route.dependant is not None:
                            _route.dependant.call = _wrapped_index
                        from fastapi.routing import APIRoute
                        from starlette.routing import request_response
                        if isinstance(_route, APIRoute):
                            _route.app = request_response(_route.get_route_handler())
                        print("[WRAPPER] Hooked / route to serve frontend_extracted.html successfully.", file=sys.stderr)
                    break
    except Exception as _hook_err:
        print(f"[WRAPPER] Warning: could not install hooks: {_hook_err}", file=sys.stderr)

# ─────────────────────────────────────────────────────────────────────────────
# Wrap uvicorn.run to intercept FastAPI app creation and modify routes
# ─────────────────────────────────────────────────────────────────────────────
import uvicorn
_real_uvicorn_run = uvicorn.run

def _wrapped_uvicorn_run(*args, **kwargs):
    _install_routes_and_hooks()
    return _real_uvicorn_run(*args, **kwargs)

uvicorn.run = _wrapped_uvicorn_run

# IMPORTANT: Set _rvc_exec_globals BEFORE exec()
builtins._rvc_exec_globals = _globals

# Remove old gr.Tab hook
# IMPORTANT: Set _rvc_exec_globals BEFORE exec()
builtins._rvc_exec_globals = _globals

exec(_code, _globals)

# Worker process hook
_install_routes_and_hooks()

