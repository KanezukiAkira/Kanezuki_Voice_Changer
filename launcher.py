import os
import sys
import subprocess
import time
import zipfile
import shutil
import uuid

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

VERSION_FILE = "version.txt"
UPDATE_URL = "https://raw.githubusercontent.com/KanezukiAkira/Kanezuki_Voice_Changer/main/version.json"
REPO_ZIP_URL = "https://github.com/KanezukiAkira/Kanezuki_Voice_Changer/archive/refs/heads/main.zip"

def show_error_msg(title, message):
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        print(f"\n[LỖI CRITICAL] {title}: {message}\n")

def cleanup_old_files():
    print("[UPDATER] Đang dọn dẹp các tệp tin tạm cũ...")
    # Walk through the directory and remove any .old files
    for root, dirs, files in os.walk("."):
        if "runtime" in root or ".git" in root or ".github" in root:
            continue
        for file in files:
            if file.endswith(".old"):
                path = os.path.join(root, file)
                try:
                    os.remove(path)
                except Exception:
                    pass
    
    # Delete legacy plain infer-web.py if it exists
    if os.path.exists("infer-web.py"):
        try:
            os.remove("infer-web.py")
            print("[UPDATER] Đã xóa file infer-web.py cũ để bảo mật")
        except Exception:
            pass

def check_for_updates():
    print("[UPDATER] Đang kiểm tra cập nhật...")
    try:
        import requests
        
        current_version = "1.0"
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, "r") as f:
                current_version = f.read().strip()
                
        response = requests.get(UPDATE_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # --- REMOTE KILL SWITCH ---
            if data.get("disabled", False):
                msg = data.get("disable_msg", "Phần mềm đã bị vô hiệu hóa bởi nhà phát triển.")
                show_error_msg("Thông báo", msg)
                sys.exit(0)
                
            latest_version = data.get("version", current_version)
            if latest_version != current_version:
                print(f"[UPDATER] Phát hiện phiên bản mới: {latest_version} (Hiện tại: {current_version}). Đang tải...")
                
                zip_path = "update_temp.zip"
                r = requests.get(REPO_ZIP_URL, stream=True)
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                print("[UPDATER] Đang cài đặt bản cập nhật bằng Safe Rename...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Github zip contains Kanezuki_Voice_Changer-main/
                    for member in zip_ref.namelist():
                        if member.startswith("Kanezuki_Voice_Changer-main/"):
                            target_path = member.replace("Kanezuki_Voice_Changer-main/", "", 1)
                            if target_path and not member.endswith('/'):
                                # Create directories if they don't exist
                                dir_name = os.path.dirname(target_path)
                                if dir_name:
                                    os.makedirs(dir_name, exist_ok=True)
                                
                                # Safe Overwrite: Rename existing file first
                                if os.path.exists(target_path):
                                    old_path = f"{target_path}.{uuid.uuid4().hex[:6]}.old"
                                    try:
                                        os.rename(target_path, old_path)
                                    except Exception as e:
                                        print(f"[UPDATER] Cảnh báo: Không thể đổi tên file cũ {target_path} -> {old_path}: {e}")
                                
                                # Write new file content
                                try:
                                    with zip_ref.open(member) as source, open(target_path, "wb") as target:
                                        shutil.copyfileobj(source, target)
                                except Exception as e:
                                    print(f"[UPDATER] Lỗi ghi đè file {target_path}: {e}")
                                    
                os.remove(zip_path)
                
                with open(VERSION_FILE, "w") as f:
                    f.write(latest_version)
                    
                print("[UPDATER] Cập nhật hoàn tất! Đang khởi động lại ứng dụng...")
                # Restart the launcher immediately
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("[UPDATER] Bạn đang sử dụng phiên bản mới nhất.")
    except Exception as e:
        print(f"[UPDATER] Lỗi kiểm tra cập nhật: {e}")

def run_app():
    print("[APP] Đang khởi động RVC Core...")
    python_cmd = os.path.join("runtime", "python.exe") if os.path.exists(os.path.join("runtime", "python.exe")) else "python"
    
    # Run run_backend.py instead of infer-web.py
    backend_script = "run_backend.py" if os.path.exists("run_backend.py") else "infer-web.py"
    
    process = subprocess.Popen(
        [python_cmd, backend_script, "--pycmd", python_cmd, "--port", "7897"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=sys.stdout, 
        stderr=sys.stderr
    )

    print("[APP] Chờ RVC khởi động...")
    import socket
    for _ in range(120):
        try:
            with socket.create_connection(("127.0.0.1", 7897), timeout=1):
                break
        except OSError:
            time.sleep(1)

    import webview
    window = webview.create_window(
        'Kanezuki Voice Changer (New UI)', 
        url='http://127.0.0.1:7897/',
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
    # Ensure requests and webview are installed first
    try:
        import requests
        import webview
    except ImportError:
        python_cmd = os.path.join("runtime", "python.exe") if os.path.exists(os.path.join("runtime", "python.exe")) else "python"
        print("[LỖI] Thiếu thư viện. Đang tự động cài đặt...")
        subprocess.check_call([python_cmd, "-m", "pip", "install", "pywebview", "requests"])
        
    cleanup_old_files()
    check_for_updates()
    run_app()
