# build_obfuscated.py
import os
import shutil
import subprocess
import sys

# Reconfigure stdout/stderr to UTF-8
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# Define files to obfuscate
critical_files = ["infer_web.py", "rvc_backend.py", "launcher.py", "run_backend.py"]
runtime_py = os.path.join("runtime", "python.exe")
pyarmor_path = os.path.join("runtime", "Scripts", "pyarmor.exe")

if not os.path.exists(pyarmor_path):
    pyarmor_path = "pyarmor"  # fallback to PATH


def main():
    print("[BUILD] Bắt đầu quá trình mã hóa bảo mật nguồn...")

    # 1. Ensure infer_web.py exists (copied from infer-web.py if not already done)
    if not os.path.exists("infer_web.py") and os.path.exists("infer-web.py"):
        print("[BUILD] Copying infer-web.py to infer_web.py...")
        shutil.copy("infer-web.py", "infer_web.py")

    for f in critical_files:
        if not os.path.exists(f):
            print(f"[ERROR] Không tìm thấy file cần mã hóa: {f}")
            sys.exit(1)

    # 2. Backup raw files to a safe folder src_backup/
    backup_dir = "src_backup"
    os.makedirs(backup_dir, exist_ok=True)
    for f in critical_files:
        print(f"[BUILD] Sao lưu file gốc: {f} -> {backup_dir}/{f}")
        shutil.copy(f, os.path.join(backup_dir, f))

    # 3. Clean previous build dist/ folder
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    # 4. Run PyArmor to obfuscate
    print("[BUILD] Đang chạy PyArmor để làm rối và mã hóa code...")
    try:
        subprocess.run([pyarmor_path, "gen"] + critical_files, check=True)
    except Exception as e:
        print(f"[ERROR] Chạy PyArmor thất bại: {e}")
        sys.exit(1)

    # 5. Copy obfuscated files and runtime helper from dist/ back to root
    print("[BUILD] Đang chuyển đổi các file mã hóa về thư mục gốc...")

    # Copy obfuscated script files
    for f in critical_files:
        src_dist = os.path.join("dist", f)
        if os.path.exists(src_dist):
            shutil.copy(src_dist, f)
            print(f"[BUILD] Đã ghi đè file mã hóa: {f}")

    # Copy pyarmor_runtime directory
    dist_dirs = [d for d in os.listdir("dist") if d.startswith("pyarmor_runtime_")]
    if dist_dirs:
        pyarmor_runtime_dir = dist_dirs[0]
        src_runtime_dir = os.path.join("dist", pyarmor_runtime_dir)
        dest_runtime_dir = os.path.join(".", pyarmor_runtime_dir)

        # Remove old runtime dir if exists in root
        if os.path.exists(dest_runtime_dir):
            shutil.rmtree(dest_runtime_dir)

        shutil.copytree(src_runtime_dir, dest_runtime_dir)
        print(f"[BUILD] Đã sao chép thư viện runtime: {pyarmor_runtime_dir}")
    else:
        print("[ERROR] Không tìm thấy thư mục pyarmor_runtime trong dist!")
        sys.exit(1)

    # 6. Clean up dist/ folder
    shutil.rmtree("dist")

    # 7. Delete infer-web.py (to prevent duplicate files and force launcher to use infer_web.py/run_backend.py)
    if os.path.exists("infer-web.py"):
        os.remove("infer-web.py")
        print("[BUILD] Đã xóa file infer-web.py gốc để bảo mật")

    print(
        "[SUCCESS] Đã mã hóa xong! Các file trong thư mục gốc hiện tại đã được bảo mật."
    )
    print(
        "[INFO] Mã nguồn gốc chưa mã hóa đã được lưu trữ an toàn trong thư mục 'src_backup/'."
    )


if __name__ == "__main__":
    main()
