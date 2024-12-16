# EC-Recommend-System

- Hệ thống chính phát triển nằm trong folder: `API`
- Hệ thống gợi ý sản phẩm cá nhân hóa cho các website phần mềm Thương Mai Điện Tử.

# Thành phần hệ thống

1. Ngôn ngữ sử dụng: `Python`
2. Mô hình quản lý:`modular design`
3. Các thư viện chính sử dụng:

- FastAPI ( `Sử dụng làm quản lý chính trong việc tạo ra các routers xử lý api` )
- RapidFuzz ( `Sử dụng để phân tích đưa ra kết quả dành cho việc tìm kiếm sp` )
- TensorFlow ( `Sử dụng để xử lý các công việc của AI` )
- mysql ( `Sử dụng để kết nối cơ sở dữ liệu` )
- redis ( `Sử dụng trong việc lưu các cache dữ liệu` )
- Surprise ( `Sử dụng để xử lý các công việc của AI` )

# Tính năng

- Có sẵn các api cơ bản xử lý các tác vụ của một hệ thống gợi ý.
- Có hệ thống tùy chỉnh cho phép người dùng có thể huấn luyện và tạo nhiều loại mô hình huấn luyện cách đơn giản thông qua cài đặt tùy chỉnh theo định dạng file `yml`.
- Có sử dụng Redis dành cho việc tối ưu hóa các truy vấn đến từ database.
- Các Database hỗ trợ: `MYSQL`

# Tương lai

- Do hệ thống được phát triển trong thời gian khá ngắn nên sẽ có nhiều thiếu sót về mặt tối ưu cũng như các tính năng nâng cao có thể còn thiếu ở một hệ thống gợi ý thương mai.
- Cần có hỗ trợ nhiều loại Database hơn.
- Cần có một khung quản lý các routers từ các ngôn ngữ tốt hơn thay vì `Python` có thể là từ `Golang` và các ngôn ngữ khác.
