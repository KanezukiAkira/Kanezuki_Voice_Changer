; File cấu hình Inno Setup Compiler cho Kanezuki
[Setup]
; Tên phần mềm và thông tin
AppName=Kanezuki 
AppVersion=1.0.0
AppPublisher=Kanezuki
AppCopyright=Copyright (C) 2024
; Thư mục cài đặt mặc định (C:\Program Files\Kanezuki)
DefaultDirName={autopf}\Kanezuki
DefaultGroupName=Kanezuki
; Tên file cài đặt đầu ra
OutputDir=Output
OutputBaseFilename=Setup_Kanezuki_Secure_v1.0
; Chuẩn nén (Ultra64 giúp nén nhỏ nhất có thể)
Compression=lzma2/ultra64
SolidCompression=yes
; Chỉ hỗ trợ 64-bit
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
; Yêu cầu quyền admin để cài đặt
PrivilegesRequired=admin

[Tasks]
; Cho phép chọn tạo biểu tượng ngoài màn hình Desktop
Name: "desktopicon"; Description: "Tạo biểu tượng ngoài màn hình Desktop (Create a desktop shortcut)"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; Thêm toàn bộ các file/thư mục trong dự án vào bản cài đặt
; Lưu ý: Đã loại trừ (Excludes) các file rác của lập trình viên và git
Source: "runtime\*"; DestDir: "{app}\runtime"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "runtime\*,.git\*,.github\*,.aider*,TEMP\*,__pycache__\*,logs\*,Output\*,*.iss,*.zip,*.log,src_backup\*"

[Icons]
; Tạo shortcut trong Start Menu
Name: "{group}\Kanezuki"; Filename: "{app}\RVC-Launcher.exe"
Name: "{group}\Gỡ cài đặt Kanezuki"; Filename: "{uninstallexe}"
; Tạo shortcut ngoài Desktop
Name: "{autodesktop}\Kanezuki"; Filename: "{app}\RVC-Launcher.exe"; Tasks: desktopicon

[Run]
; Tự động chạy app sau khi cài đặt xong
Filename: "{app}\RVC-Launcher.exe"; Description: "Khởi động Kanezuki ngay bây giờ"; Flags: nowait postinstall skipifsilent
