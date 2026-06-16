import sys, os
now_dir = os.getcwd()
sys.path.append(now_dir)

import rvc_backend

info, result_audio = rvc_backend.vc_single_url(
    sid=0,
    url="http://invalid.url.that.does.not.exist",
    is_uvr=False,
    uvr_model="HP2_all_vocals",
    vocal_volume=0.0,
    beat_volume=0.0,
    f0_up_key=0,
    f0_file="",
    f0_method="rmvpe",
    file_index1="",
    file_index="",
    index_rate=0.75,
    filter_radius=3,
    resample_sr=0,
    rms_mix_rate=0.25,
    protect=0.33,
    cookies_str="",
    _unused=None
)

print("INFO:", repr(info))
print("RESULT_AUDIO:", repr(result_audio))

if result_audio is not None and result_audio[1] is not None:
    tgt_sr, audio_data = result_audio
    print("Unpacked successfully!")
else:
    print("Handled as error!")
