# Câu hỏi thường gặp (FAQ) - Kanezuki Voice Changer

## Q1: Không tìm thấy file Index sau khi bấm "Huấn luyện một bước".
Nếu màn hình thông báo "Huấn luyện hoàn tất", thì mô hình đã được tạo thành công. Việc báo lỗi thiếu file Index thường là do dữ liệu huấn luyện của bạn quá lớn khiến quá trình nén Index bị tràn RAM. 
**Cách khắc phục:** Chuyển sang tab "Huấn luyện chỉ mục (Index)" và bấm chạy thủ công lại bước tạo Index.

## Q2: Không thấy mô hình trong danh sách sau khi huấn luyện xong?
Hãy bấm nút **Làm mới danh sách giọng nói** và kiểm tra lại. Nếu vẫn không thấy, hãy xem có báo lỗi nào xuất hiện trong bảng điều khiển (Console) không. 

## Q3: Làm sao để chia sẻ mô hình của tôi cho người khác?
Những file `.pth` vài trăm MB trong thư mục `logs` KHÔNG PHẢI là mô hình để chia sẻ.
Mô hình chuẩn để sử dụng là file `.pth` (nặng khoảng 60-80MB) nằm trong thư mục `assets/weights`. Bạn chỉ cần nén file này cùng với file `.index` (nếu có) thành 1 file ZIP và gửi cho người khác là họ có thể sử dụng được.

## Q4: Lỗi kết nối / Connection Error.
Bạn đã lỡ tay đóng mất cửa sổ màu đen (Console / Command Line). Hãy mở lại phần mềm.

## Q5: WebUI báo lỗi 'Expecting value: line 1 column 1 (char 0)'.
Vui lòng tắt các phần mềm Fake IP (VPN) hoặc Proxy trên máy tính rồi tải lại trang.

## Q6: Lỗi báo thiếu VRAM / Cuda out of memory.
Card đồ họa của bạn không đủ bộ nhớ để chạy tác vụ này.
- Khi **Huấn luyện**: Hãy giảm `Batch Size` xuống. (Card 4GB VRAM vẫn có thể chạy được nếu để Batch = 1).
- Khi **Tách giọng / Đổi giọng**: Bạn có thể cắt nhỏ file âm thanh ra hoặc thử dùng CPU.

## Q7: Nên để thông số "Kỷ nguyên huấn luyện" (Epoch) bao nhiêu là tốt nhất?
- Nếu dữ liệu âm thanh của bạn có nhiều tạp âm, chất lượng kém: Để 20-30 Epoch là đủ. Cố nhồi nhét thêm cũng không làm giọng hay hơn được.
- Nếu âm thanh cực kỳ sạch, chất lượng phòng thu: Bạn có thể nâng lên tới 100-200 Epoch. 

## Q8: Cần thu âm bao nhiêu phút để làm dữ liệu huấn luyện?
- Khuyến nghị: Từ 10 phút đến 50 phút.
- Nếu âm thanh tuyệt đối sạch và không lẫn tạp âm, chỉ cần 5-10 phút là đã đủ tạo ra một mô hình chất lượng cực cao. Không nên dùng dữ liệu dưới 1 phút.

## Q9: Lỗi RuntimeError: The expanded size of the tensor (17280) must match...
Lỗi này xảy ra khi có một file âm thanh rác quá ngắn hoặc bị lỗi trong thư mục dữ liệu của bạn. Hãy vào thư mục đó, xóa các file âm thanh có kích thước nhỏ bất thường rồi chạy lại.
