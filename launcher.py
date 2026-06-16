import os
import sys
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def run_app():
    print("[APP] Đang khởi động RVC Core...")
    python_cmd = os.path.join("runtime", "python.exe") if os.path.exists(os.path.join("runtime", "python.exe")) else "python"
    
    # Chạy subprocess
    process = subprocess.Popen(
        [python_cmd, "infer-web.py", "--pycmd", python_cmd, "--port", "7897"],
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
    try:
        import webview
    except ImportError:
        python_cmd = os.path.join("runtime", "python.exe") if os.path.exists(os.path.join("runtime", "python.exe")) else "python"
        subprocess.check_call([python_cmd, "-m", "pip", "install", "pywebview"])
        import webview
    
    run_app()
