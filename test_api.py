import requests

data = {
    'sid': 'Yae_MikoJP.pth',
    'audio_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'f0_up_key': '0',
    'f0_method': 'rmvpe',
    'index_rate': '0.75',
    'protect': '0.33',
    'vocal_volume': '0',
    'beat_volume': '0',
    'is_uvr': 'false',
    'file_index': '',
    'filter_radius': '3',
    'resample_sr': '0',
    'rms_mix_rate': '0.25',
    'uvr_model': 'HP2_all_vocals'
}

res = requests.post("http://127.0.0.1:7897/api/convert", data=data)
print(res.status_code)
print(res.text)
