# -*- coding: utf-8 -*-
import zlib
import base64
import os
import shutil
import sys
import py_compile

# Đảm bảo in được tiếng Việt
sys.stdout.reconfigure(encoding='utf-8')

critical_files = ['infer_web.py', 'rvc_backend.py', 'launcher.py', 'run_backend.py']
backup_dir = 'src_backup'

os.makedirs(backup_dir, exist_ok=True)

for f in critical_files:
    if os.path.exists(f):
        shutil.copy(f, os.path.join(backup_dir, f))
        with open(f, 'rb') as file:
            content = file.read()
        compressed = zlib.compress(content)
        encoded = base64.b64encode(compressed).decode('utf-8')
        obfuscated = f"import zlib, base64\nexec(zlib.decompress(base64.b64decode('{encoded}')), globals())"
        with open(f, 'w', encoding='utf-8') as file:
            file.write(obfuscated)
        print(f'[BUILD] Ma hoa co ban thanh cong: {f}')

# Biên dịch launcher.py thành launcher.pyc để RVC-Launcher.exe chạy được
if os.path.exists('launcher.py'):
    py_compile.compile('launcher.py', 'launcher.pyc')
    print('[BUILD] Bien dich launcher.pyc thanh cong')
