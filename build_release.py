import os
import subprocess
import re

def main():
    print("=== BẮT ĐẦU CHUẨN BỊ ĐÓNG GÓI BẢO MẬT ===")
    
    # 1. Dùng Python trong runtime để biên dịch toàn bộ code .py sang .pyc
    print("1. Đang biên dịch mã nguồn sang dạng mã hóa (.pyc)...")
    python_exe = os.path.join("runtime", "python.exe")
    if not os.path.exists(python_exe):
        print(f"Không tìm thấy {python_exe}. Đang dùng python hệ thống...")
        python_exe = "python"
        
    # Dùng cờ -b để tạo file .pyc nằm cùng thư mục với .py (thay vì trong __pycache__)
    # Dùng cờ -x để bỏ qua thư mục runtime (tránh biên dịch lại thư viện chuẩn)
    subprocess.run([python_exe, "-m", "compileall", "-b", "-x", r"runtime|\.git|\.github", "."], check=True)
    print("   -> Đã biên dịch xong!")
    
    # 2. Tạo file go-web-release.bat mới
    print("\n2. Tạo file chạy go-web-release.bat...")
    with open("go-web-release.bat", "w", encoding="utf-8") as f:
        f.write("runtime\\python.exe launcher.pyc\npause\n")
    print("   -> Đã tạo go-web-release.bat")
        
    # 3. Tạo file Inno Setup mới (loại bỏ file .py)
    print("\n3. Tạo cấu hình cài đặt build_setup_release.iss...")
    if not os.path.exists("build_setup.iss"):
        print("Lỗi: Không tìm thấy build_setup.iss gốc.")
        return
        
    with open("build_setup.iss", "r", encoding="utf-8") as f:
        iss_content = f.read()
        
    # Thêm *.py vào danh sách loại trừ để không đóng gói mã nguồn gốc
    if "Excludes: " in iss_content:
        iss_content = iss_content.replace("Excludes: ", "Excludes: *.py,")
    else:
        # Thay thế DestDir: "{app}"; thành DestDir: "{app}"; Excludes: *.py;
        iss_content = re.sub(r'(DestDir:\s*"{app}";?)', r'\1 Excludes: *.py;', iss_content)
        
    # Đổi tên file output để không trùng với bản cũ
    iss_content = iss_content.replace("OutputBaseFilename=Setup_Kanezuki_v1.0", "OutputBaseFilename=Setup_Kanezuki_Secure_v1.0")
    
    # Đổi file chạy từ go-web.bat thành go-web-release.bat
    iss_content = iss_content.replace("go-web.bat", "go-web-release.bat")
    
    with open("build_setup_release.iss", "w", encoding="utf-8") as f:
        f.write(iss_content)
    print("   -> Đã tạo build_setup_release.iss")
        
    print("\n=== HOÀN TẤT ===")
    print("Bây giờ bạn hãy làm theo các bước sau:")
    print("1. Bạn có thể click đúp vào file 'go-web-release.bat' để test thử xem phần mềm chạy ở dạng .pyc có bình thường không.")
    print("2. Mở file 'build_setup_release.iss' bằng Inno Setup và nhấn nút Compile (nút mũi tên xanh hoặc Ctrl+F9) để tạo bộ cài.")

if __name__ == "__main__":
    main()
