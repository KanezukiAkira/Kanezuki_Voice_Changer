import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import builtins
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import soundfile as sf
import uuid

# Import RVC logic
import rvc_backend

from configs.config import Config
from infer.modules.vc.modules import VC
from configs.config import Config
from infer.modules.vc.modules import VC
from infer.modules.vc.modules import VC

# Initialize global VC object
config = Config()
vc_obj = VC(config)
builtins._rvc_exec_globals = {'vc': vc_obj}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/outputs", exist_ok=True)
os.makedirs("TEMP", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/models")
def get_models():
    models = rvc_backend.scan_models()
    return {"models": list(models.keys())}

@app.post("/api/load_model")
def load_model(sid: str = Form(...)):
    models = rvc_backend.scan_models()
    if sid not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    pth_path, idx_path = models[sid]
    weight_root = os.getenv("weight_root", "assets/weights")
    rel_pth = pth_path
    if pth_path.startswith(weight_root):
        rel_pth = pth_path[len(weight_root):].lstrip("/\\")
    
    result = vc_obj.get_vc(rel_pth)
    info = result[0] if isinstance(result, tuple) else result
    return {"status": "success", "info": info, "index_path": idx_path}

from typing import Optional

@app.post("/api/convert")
async def convert(
    audio: Optional[UploadFile] = File(None),
    audio_url: str = Form(""),
    sid: str = Form(""), # Use currently loaded model by default
    f0_up_key: int = Form(0),
    f0_method: str = Form("rmvpe"),
    file_index: str = Form(""),
    index_rate: float = Form(0.75),
    filter_radius: int = Form(3),
    resample_sr: int = Form(0),
    rms_mix_rate: float = Form(0.25),
    protect: float = Form(0.33),
    is_uvr: bool = Form(False),
    uvr_model: str = Form("HP2_all_vocals"),
    vocal_volume: float = Form(0),
    beat_volume: float = Form(0)
):
    try:
        if vc_obj.pipeline is None and sid:
            # Try to load model on the fly if not loaded
            load_model(sid)
            
        if vc_obj.pipeline is None:
            return JSONResponse(status_code=400, content={"error": "Vui lòng chọn model trước khi convert!"})

        if audio_url and audio_url.strip():
            info, result_audio = rvc_backend.vc_single_url(
                sid=0,
                url=audio_url.strip(),
                is_uvr=is_uvr,
                uvr_model=uvr_model,
                vocal_volume=vocal_volume,
                beat_volume=beat_volume,
                f0_up_key=f0_up_key,
                f0_file="",
                f0_method=f0_method,
                file_index1="",
                file_index=file_index,
                index_rate=index_rate,
                filter_radius=filter_radius,
                resample_sr=resample_sr,
                rms_mix_rate=rms_mix_rate,
                protect=protect,
                cookies_str="",
                _unused=None
            )
        else:
            if not audio:
                return JSONResponse(status_code=400, content={"error": "Vui lòng chọn file âm thanh hoặc nhập URL"})
                
            # Save uploaded audio
            temp_input = os.path.join("TEMP", f"input_{uuid.uuid4().hex}_{audio.filename}")
            with open(temp_input, "wb") as f:
                f.write(await audio.read())

            info, result_audio = rvc_backend.vc_single_local(
                sid=0, # Use global vc_obj
                model_name_hint="",
                input_audio_path=temp_input,
                is_uvr=is_uvr,
                uvr_model=uvr_model,
                vocal_volume=vocal_volume,
                beat_volume=beat_volume,
                f0_up_key=f0_up_key,
                f0_file="",
                f0_method=f0_method,
                file_index1="",
                file_index=file_index,
                index_rate=index_rate,
                filter_radius=filter_radius,
                resample_sr=resample_sr,
                rms_mix_rate=rms_mix_rate,
                protect=protect
            )

        if result_audio is None or result_audio[1] is None:
            return JSONResponse(status_code=500, content={"error": info})

        tgt_sr, audio_data = result_audio
        out_filename = f"output_{uuid.uuid4().hex}.wav"
        out_path = os.path.join("static", "outputs", out_filename)
        
        sf.write(out_path, audio_data, tgt_sr)
        
        if not audio_url:
            try:
                os.remove(temp_input)
            except:
                pass

        return {"info": info, "audio_url": f"/static/outputs/{out_filename}"}

    except Exception as e:
        import traceback
        return JSONResponse(status_code=500, content={"error": str(e), "trace": traceback.format_exc()})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7897)
