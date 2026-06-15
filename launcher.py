import os
import sys
import subprocess
import time
import requests
import json
import threading

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ---------------------------------------------------------
# 1. TỰ ĐỘNG CẬP NHẬT (AUTO-UPDATER)
# ---------------------------------------------------------
VERSION_FILE = "version.txt"
UPDATE_URL = "https://raw.githubusercontent.com/KanezukiAkira/Kanezuki_Voice_Changer/main/version.json"
REPO_ZIP_URL = "https://github.com/KanezukiAkira/Kanezuki_Voice_Changer/archive/refs/heads/main.zip"

def check_for_updates():
    print("[UPDATER] Đang kiểm tra cập nhật...")
    try:
        current_version = "1.0"
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, "r") as f:
                current_version = f.read().strip()
        
        response = requests.get(UPDATE_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # ----------------------------------------------
            # CHỨC NĂNG KILL SWITCH (VÔ HIỆU HÓA TỪ XA)
            # ----------------------------------------------
            if data.get("disabled", False):
                # Nếu bạn set "disabled": true trên Github, app sẽ báo lỗi và tự tắt
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Thông báo", data.get("disable_msg", "Phần mềm đã bị vô hiệu hóa bởi nhà phát triển."))
                sys.exit(0)

            latest_version = data.get("version", current_version)
            if latest_version > current_version:
                print(f"[UPDATER] Đã có phiên bản mới: {latest_version}. Đang tiến hành tải dữ liệu...")
                
                # Tải file ZIP mã nguồn mới nhất từ Github
                zip_path = "update_temp.zip"
                r = requests.get(REPO_ZIP_URL, stream=True)
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print("[UPDATER] Tải xong! Đang cài đặt bản cập nhật...")
                import zipfile
                import shutil
                # Giải nén đè lên các file hiện hành
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # File tải từ Github thường bọc trong thư mục Kanezuki_Voice_Changer-main
                    for member in zip_ref.namelist():
                        if member.startswith("Kanezuki_Voice_Changer-main/"):
                            # Bỏ qua folder gốc
                            target_path = member.replace("Kanezuki_Voice_Changer-main/", "", 1)
                            if target_path and not member.endswith('/'):
                                # Chỉ ghi đè các file không bị khóa
                                try:
                                    os.makedirs(os.path.dirname(target_path) or ".", exist_ok=True)
                                    with zip_ref.open(member) as source, open(target_path, "wb") as target:
                                        shutil.copyfileobj(source, target)
                                except Exception as write_err:
                                    print(f"Bỏ qua file đang được dùng: {target_path}")

                os.remove(zip_path) # Xóa file rác
                
                print("[UPDATER] Đang biên dịch mã nguồn mới ra file ẩn mã (.pyc)...")
                python_exe = os.path.join("runtime", "python.exe") if os.path.exists(os.path.join("runtime", "python.exe")) else sys.executable
                try:
                    subprocess.run([python_exe, "-m", "compileall", "-b", "-x", r"runtime|\.git|\.github", "."], check=False)
                    # Xóa các file .py vừa tải về để bảo mật code
                    for root_dir, dirs, files in os.walk("."):
                        if "runtime" in root_dir or ".git" in root_dir:
                            continue
                        for file in files:
                            if file.endswith(".py"):
                                try:
                                    os.remove(os.path.join(root_dir, file))
                                except:
                                    pass
                except Exception as e:
                    print(f"[UPDATER] Lỗi khi biên dịch: {e}")
                
                # Lưu lại phiên bản mới
                with open(VERSION_FILE, "w") as f:
                    f.write(latest_version)
                print("[UPDATER] Cập nhật thành công! Chuẩn bị chạy phần mềm...")
            else:
                print("[UPDATER] Phiên bản đang dùng là mới nhất.")
    except Exception as e:
        print(f"[UPDATER] Không thể kiểm tra cập nhật ngay lúc này: {e}")

# ---------------------------------------------------------
# 2. KIỂM TRA KẾT NỐI MẠNG (BẮT BUỘC)
# ---------------------------------------------------------
def check_internet():
    try:
        requests.get("https://8.8.8.8", timeout=2)
        return True
    except:
        return False

# ---------------------------------------------------------
# 3. CHẠY ỨNG DỤNG RVC VÀ GIAO DIỆN
# ---------------------------------------------------------
def run_app():
    if not check_internet():
        print("LỖI: Bạn phải kết nối Internet để sử dụng phần mềm này!")
        input("Nhấn Enter để thoát...")
        sys.exit(1)

    print("[APP] Đang khởi động RVC Core...")
    # Khởi chạy infer-web.py dưới nền ẩn
    python_cmd = os.path.join("runtime", "python.exe") if os.path.exists(os.path.join("runtime", "python.exe")) else "python"
    
    # Chạy subprocess
    process = subprocess.Popen(
        [python_cmd, "infer-web.pyc", "--pycmd", python_cmd, "--port", "7897"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )

    print("[APP] Chờ RVC khởi động (có thể mất một lúc ở lần đầu)...")
    import socket
    for _ in range(120):
        try:
            with socket.create_connection(("127.0.0.1", 7897), timeout=1):
                break
        except OSError:
            time.sleep(1)

    import webview
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, "wrapper.html")
    
    window = webview.create_window(
        'Voice Changer - Powered by Aki', 
        url=f'file:///{html_path}',
        width=1200, 
        height=800,
        resizable=True
    )
    
    print("[APP] Mở giao diện thành công.")
    webview.start()

    print("[APP] Đang đóng phần mềm...")
    process.terminate()
    process.wait()
    sys.exit(0)

if __name__ == "__main__":
    check_for_updates()
    try:
        import webview
    except ImportError:
        print("[LỖI] Thiếu thư viện pywebview.")
        print("Đang tự động cài đặt...")
        python_cmd = os.path.join("runtime", "python.exe") if os.path.exists(os.path.join("runtime", "python.exe")) else "python"
        subprocess.check_call([python_cmd, "-m", "pip", "install", "pywebview", "requests"])
        import webview
    
    run_app()
