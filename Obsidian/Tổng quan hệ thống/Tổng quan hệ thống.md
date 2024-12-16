
Ngôn ngữ sử dụng: `Python`
Mô hình quản lý: `modular design`
Các thư viện chính sử dụng: 
- FastAPI ( `Sử dụng làm quản lý chính trong việc tạo ra các routers xử lý api` )
- RapidFuzz ( `Sử dụng để phân tích đưa ra kết quả dành cho việc tìm kiếm sp` )
- TensorFlow ( `Sử dụng để xử lý các công việc của AI` )
- mysql ( `Sử dụng để kết nối cơ sở dữ liệu` )
- redis ( `Sử dụng trong việc lưu các cache dữ liệu` )
- Surprise ( `Sử dụng để xử lý các công việc của AI` )

Tính năng hệ thống:
- Có hệ thống quản lý các cài đặt trong hệ thống bằng file `config.yml`
- Có hệ thống quản lý ghi lại các trạng thái trong hệ thống hằng ngày.
- Có tính năng áp dụng cho **gần như** đa mô hình cơ sở dữ liệu.
- Sử dụng Redis để lưu bộ nhớ cache giúp truy vấn và xử lý nhanh các truy vấn từ phía cơ sở dữ liệu. 
- Tính năng xử lý gợi ý:
	- Xử lý gợi ý dựa trên kết quả đầu vào ví dụ như một từ hoặc cụm từ để đưa ra các danh sách tên sản phẩm có thể gợi ý trong máy chủ.
	- Xử lý gợi ý cho 1 người dùng đã đăng nhập hoặc đã có thông tin trên cơ sở dữ liệu bằng kết quả phân tích từ mô hình máy học.
	- Gợi ý sản phẩm theo chiến lược thiết kế tùy chỉnh của người dùng dựa trên tên 1 cột hoặc nhiều cột mà người dùng muốn chọn (Ví dụ như: ngày tháng, giảm giá, ...)

Mô hình AI: 
- Loại thuật toán: `Collaborative Filtering sử dụng **Matrix Factorization** trong Python`
- Có thời gian đặt ra để huấn luyện theo thời gian thực. Có thể cấu hình thời gian này trên file cấu hình của hệ thống.

Hạn chế:
- Thời gian hoàn thành dự án có hạn nên trong tương lai sẽ cần phải áp dụng tối ưu các truy vấn hoặc xử lý các dữ liệu trong hệ thống cần phải cải thiện và tính năng mới có thể sẽ có trong tương lai.