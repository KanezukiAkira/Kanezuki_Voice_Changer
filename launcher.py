import os
import sys
import subprocess
import time
import requests
import json
import threading

# ---------------------------------------------------------
# 1. TỰ ĐỘNG CẬP NHẬT (AUTO-UPDATER)
# ---------------------------------------------------------
VERSION_FILE = "version.txt"
UPDATE_URL = "https://raw.githubusercontent.com/YourUsername/YourRepo/main/version.json" # Thay bằng link Github của bạn

def check_for_updates():
    print("[UPDATER] Đang kiểm tra cập nhật...")
    try:
        # Lấy version hiện tại
        current_version = "1.0"
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, "r") as f:
                current_version = f.read().strip()
        
        # Thử lấy version mới nhất từ internet
        # LƯU Ý: Chức năng này tạm thời bị tắt (try/except bỏ qua) 
        # cho đến khi bạn thay thế UPDATE_URL bằng link thật.
        response = requests.get(UPDATE_URL, timeout=3)
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("version", current_version)
            if latest_version > current_version:
                print(f"[UPDATER] Đã có phiên bản mới: {latest_version}. Đang tải...")
                # Code tải các file cập nhật sẽ viết ở đây
                # ... (ví dụ: dùng requests để tải file infer-web.py mới)
                
                # Cập nhật lại version.txt
                with open(VERSION_FILE, "w") as f:
                    f.write(latest_version)
                print("[UPDATER] Cập nhật thành công!")
            else:
                print("[UPDATER] Phiên bản đang dùng là mới nhất.")
    except Exception as e:
        print(f"[UPDATER] Không thể kiểm tra cập nhật (Không có mạng hoặc Sai URL): {e}")

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
        stdout=subprocess.DEVNULL, # Ẩn log của RVC đi cho gọn (hoặc bỏ dòng này nếu muốn xem log)
        stderr=subprocess.DEVNULL
    )

    print("[APP] Chờ RVC khởi động (khoảng 5 giây)...")
    time.sleep(5) # Đợi 5 giây cho cổng 7897 mở lên

    # Bật giao diện Desktop chứa Quảng Cáo
    import webview
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, "wrapper.html")
    
    # Tạo cửa sổ
    window = webview.create_window(
        'Voice Changer - Powered by Aki', 
        url=f'file:///{html_path}',
        width=1200, 
        height=800,
        resizable=True
    )
    
    print("[APP] Mở giao diện thành công.")
    webview.start()

    # Khi người dùng tắt cửa sổ, kill cái process RVC ẩn đi
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
