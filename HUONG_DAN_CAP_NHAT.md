# Hướng dẫn Chỉnh sửa và Cập nhật Ứng dụng (Cho Nhà phát triển)

Tài liệu này hướng dẫn chi tiết quy trình chỉnh sửa mã nguồn, mã hóa bảo mật bằng PyArmor, đẩy cập nhật lên GitHub và đóng gói file cài đặt `.exe`.

---

## 1. Sơ đồ quy trình phát triển và phát hành

```
[Chỉnh sửa code gốc trong src_backup/] 
                │
                ▼
[Chạy build_obfuscated.py để mã hóa] (Tạo code ẩn trong thư mục gốc)
                │
         ┌──────┴──────┐
         ▼             ▼
  [Đẩy lên GitHub]  [Đóng gói bộ cài với Inno Setup]
  (Auto-update)     (Cho người dùng mới)
```

---

## 2. Quy trình chỉnh sửa mã nguồn (Code Modification)

Vì các tệp tin trong thư mục gốc đã được mã hóa làm rối để bảo mật (ở dạng nhị phân mã hóa), bạn **không chỉnh sửa trực tiếp** các tệp đó. 

Hãy làm theo các bước sau để sửa code:

1. **Bước 1: Sửa code gốc**
   * Mở thư mục [src_backup/](file:///c:/Users/sonho/Downloads/Vtuber_Aki/RVC1006Nvidia%20-%20Copy/src_backup/)
   * Chỉnh sửa logic tính năng trong các tệp gốc chưa mã hóa: `infer_web.py` hoặc `rvc_backend.py` tại đây.

2. **Bước 2: Chép file đã sửa ra ngoài**
   * Sao chép các tệp vừa sửa từ thư mục `src_backup/` ra ngoài thư mục gốc của dự án (ghi đè lên các tệp mã hóa cũ).

3. **Bước 3: Chạy mã hóa bảo mật**
   * Mở Terminal/Command Prompt tại thư mục dự án và chạy lệnh sau:
     ```bash
     runtime\python.exe build_obfuscated.py
     ```
   * **Kết quả:** Lệnh này sẽ tự động:
     * Lưu bản sao code gốc mới nhất vào lại `src_backup/`.
     * Tiến hành chạy PyArmor mã hóa và ghi đè các tệp `.py` ở thư mục gốc thành tệp bảo mật.
     * Cập nhật thư viện runtime của PyArmor.

---

## 3. Quy trình phát hành cập nhật cho người dùng (Auto-Update)

Khi bạn muốn người dùng tự động nhận bản cập nhật mới khi mở app:

1. **Bước 1: Tăng số phiên bản**
   * Mở tệp [version.txt](file:///c:/Users/sonho/Downloads/Vtuber_Aki/RVC1006Nvidia%20-%20Copy/version.txt) cục bộ và sửa số phiên bản (Ví dụ từ `1.0` lên `1.1`).
   * Sửa tệp [version.json](file:///c:/Users/sonho/Downloads/Vtuber_Aki/RVC1006Nvidia%20-%20Copy/version.json) cục bộ tương ứng:
     * `"version": "1.1"`
     * Cập nhật nhật ký thay đổi trong `"changelog"`.

2. **Bước 2: Đẩy code lên GitHub**
   * Thực hiện các lệnh Git để đẩy toàn bộ code đã mã hóa lên repository GitHub của bạn:
     ```bash
     git add .
     git commit -m "Cập nhật tính năng X và tăng phiên bản lên 1.1"
     git push origin main
     ```
   * **Lưu ý:** Thư mục chứa code thô chưa mã hóa (`src_backup/`) đã được cấu hình tự động bỏ qua trong `.gitignore`, đảm bảo code gốc của bạn không bao giờ bị lộ lên GitHub.

3. **Kết quả:** Người dùng khi mở app lên, `launcher.py` sẽ so sánh phiên bản và tự động tải ZIP bản mới từ GitHub về ghi đè, dọn dẹp các tệp cũ không lỗi.

---

## 4. Quy trình đóng gói bộ cài đặt mới (Build Setup Installer)

Dành cho người dùng tải app lần đầu (không cần tải qua GitHub):

1. **Bước 1:** Chạy mã hóa code thô trước bằng `build_obfuscated.py`.
2. **Bước 2:** Mở trình biên dịch **Inno Setup Compiler** trên máy của bạn.
3. **Bước 3:** Mở tệp cấu hình [build_setup_release.iss](file:///c:/Users/sonho/Downloads/Vtuber_Aki/RVC1006Nvidia%20-%20Copy/build_setup_release.iss) trong Inno Setup.
4. **Bước 4:** Nhấn nút **Compile (hoặc Ctrl + F9)** để tiến hành đóng gói.
5. **Kết quả:** File cài đặt hoàn chỉnh `Setup_Kanezuki_Secure_v1.1.exe` sẽ được tạo ra tại thư mục `Output/` của dự án. Gửi file cài đặt này cho người dùng mới.

---

## 5. Nhật ký cập nhật & Kết quả triển khai (Phiên bản 1.1)

Dưới đây là chi tiết các tính năng mới đã được triển khai và kiểm thử thành công trong phiên bản **1.1**:

### Các tính năng đã triển khai:
* **Hộp thoại lưu tệp Windows gốc (Windows Save As Dialog):**
  * Khi người dùng nhấn nút **Tải về máy** trên giao diện, frontend sẽ gọi API `/api/save_audio`.
  * Backend mở hộp thoại chọn đường dẫn lưu tệp native của Windows. Người dùng có thể tự do đặt tên và chọn nơi lưu (Desktop, ổ D, thư mục Nhạc,...).
  * Tệp tin sẽ tự động được sao chép sang vị trí đã chọn.
  * Thêm cơ chế xác thực tên tệp an toàn (phải bắt đầu bằng `output_` và kết thúc bằng `.wav`) để tránh lỗ hổng bảo mật.

* **Chuyển tệp kết quả tạm sang thư mục TEMP:**
  * Không ghi các tệp âm thanh chuyển đổi vào thư mục `static/outputs/` của dự án để tránh làm nặng bộ cài và làm xáo trộn mã nguồn.
  * Ghi tệp vào thư mục `TEMP/` (thư mục này bị bỏ qua bởi Git và bộ cài).
  * Stream trực tiếp luồng âm thanh từ `TEMP/` hiển thị lên trình phát nhạc của frontend thông qua endpoint `/api/audio/{filename}`.
  * Tự động dọn dẹp sạch sẽ toàn bộ các tệp kết quả cũ `output_*.wav` trong thư mục `TEMP/` mỗi khi backend khởi động.
  * Loại bỏ hoàn toàn phần chọn thư mục lưu (Tùy chọn) trước đó ở cột phải để tinh giản hóa giao diện.

* **Đóng gói bộ cài mới:**
  * Bộ cài đầu ra: `Output\Setup_Kanezuki_Secure_v1.1.exe`.
  * Số phiên bản ứng dụng được nâng cấp lên `1.1.0`.

* **Đồng bộ GitHub:**
  * Đã commit và push tất cả thay đổi bao gồm cả `version.json` (phiên bản `1.1` với changelog tiếng Việt) lên nhánh `main` của GitHub thành công.

