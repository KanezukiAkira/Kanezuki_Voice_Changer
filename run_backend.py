# run_backend.py
import os
import sys
import uvicorn

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the obfuscated FastAPI app
try:
    import infer_web
except ImportError as e:
    print(f"[BACKEND ERROR] Không thể nhập module backend: {e}")
    sys.exit(1)

if __name__ == "__main__":
    port = 7897
    # Read port from command line arguments if passed
    if "--port" in sys.argv:
        try:
            port = int(sys.argv[sys.argv.index("--port") + 1])
        except Exception:
            pass
            
    print(f"[BACKEND] Khởi chạy uvicorn tại cổng {port}...")
    uvicorn.run(infer_web.app, host="127.0.0.1", port=port)
