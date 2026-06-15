<div align="center">

<h1>RVC Voice Changer - Bản Tiếng Việt (Custom Web UI)</h1>
Một công cụ biến đổi giọng nói dựa trên RVC (Retrieval-based Voice Conversion) được tinh chỉnh và việt hóa giao diện, mang lại trải nghiệm dễ sử dụng nhất.<br><br>

</div>

------

## 🌟 Giới thiệu

Đây là phiên bản tùy chỉnh (Custom Build) của dự án RVC gốc, tập trung vào việc tối ưu hóa giao diện người dùng và tinh gọn hệ thống. Phiên bản này được thiết kế đặc biệt với:
- **Giao diện Web hiện đại (Frontend mới)**: Dễ nhìn, thân thiện và hoàn toàn bằng tiếng Việt.
- **Tích hợp sẵn API Server (FastAPI)**: Ổn định và phản hồi nhanh hơn giao diện Gradio cũ.
- **Dọn dẹp môi trường**: Đã loại bỏ các thư viện và tệp tin không cần thiết (Gradio, PySimpleGUI, các file Colab, cấu hình cho AMD/Intel) để giảm dung lượng, tối ưu riêng cho card đồ họa **NVIDIA**.

## ✨ Các tính năng chính

1. **Biến đổi giọng nói (Inference)**: Chuyển đổi giọng nói của bạn sang giọng của các nhân vật/ca sĩ yêu thích với độ trễ thấp và chất lượng cao (sử dụng thuật toán trích xuất âm cao RMVPE tối tân).
2. **Tách nhạc (UVR5)**: Trích xuất giọng hát (Vocal) và nhạc nền (Instrumental) từ một bài hát bất kỳ một cách nhanh chóng để làm dữ liệu huấn luyện hoặc hát karaoke.
3. **Huấn luyện mô hình (Training)**: Tự tạo mô hình giọng nói AI cho riêng bạn chỉ với khoảng 10-15 phút âm thanh giọng nói mẫu (dataset sạch).
4. **Hỏi đáp & FAQ**: Hướng dẫn chi tiết các lỗi thường gặp được tích hợp ngay trong ứng dụng.

## 🚀 Cách sử dụng

Ứng dụng đã được đóng gói sẵn môi trường (`runtime`). Bạn không cần phải cài đặt thêm Python hay cấu hình môi trường thủ công phức tạp.

1. Khởi động ứng dụng bằng cách chạy file **`RVC-Launcher.exe`** (hoặc chạy trực tiếp script `launcher.py` nếu bạn là lập trình viên).
2. Hệ thống sẽ tự động khởi động Backend Server và mở một cửa sổ Desktop hiển thị giao diện phần mềm.
3. Nếu bạn chỉ muốn khởi động Server để truy cập qua trình duyệt web ngoài, bạn có thể chạy file **`go-web.bat`**, sau đó truy cập vào `http://127.0.0.1:7897`.

## 🛠 Cấu trúc dự án
- `frontend_extracted.html`: Giao diện người dùng (HTML/CSS/JS) chính thức của phần mềm.
- `infer-web.py` / `infer-web-real.pyc`: Xử lý Backend API và các tác vụ AI lõi.
- `launcher.py`: Script khởi động giao diện Desktop bằng WebView.
- `runtime/`: Môi trường Python nội bộ chứa toàn bộ thư viện và dependencies cần thiết.
- `assets/`: Chứa các mô hình âm thanh (hubert, uvr5, rmvpe) phục vụ cho quá trình xử lý AI.

## 🙏 Ghi chú & Lời cảm ơn

Dự án này được xây dựng dựa trên mã nguồn mở cốt lõi của [RVC-Project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) và các thư viện liên quan như VITS, RMVPE. Mọi quyền đối với thuật toán lõi thuộc về các nhà phát triển gốc. Phần giao diện UI và kiến trúc API trong bản phân phối này được thiết kế và tùy chỉnh riêng biệt nhằm mang lại sự tiện lợi lớn nhất cho cộng đồng người dùng Việt Nam.
