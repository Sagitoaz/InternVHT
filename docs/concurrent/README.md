# UML cho `src/concurrent`

Thư mục này so sánh thời gian đọc và đếm dòng/từ trong file văn bản theo 5 chế độ: BUFFERED, UNBUFFERED, QUEUE, EXECUTOR và VIRTUAL. Các chế độ đồng thời còn chuyển nội dung sang chữ hoa và có thể ghi từng bản ghi. Báo cáo được append vào `results.txt` và in ra console.

Mở từng file bằng draw.io. Mỗi file chứa một sơ đồ:

- [Class diagram](class-diagram.drawio): 21 lớp chính, mỗi lớp có ba ngăn tên/thuộc tính/phương thức; có visibility, static, abstract, multiplicity và các quan hệ generalization, realization, association, composition, dependency. Chỉ vẽ các quan hệ chính, lược bỏ dependency phụ và các đường dài lặp lại; đường nối được làm đậm để dễ nhìn.
- [Sequence diagram](sequence-diagram.drawio): luồng chính từ CLI đến báo cáo; có actor, boundary/control/entity, lifeline, activation và đường trả về nét đứt. Chỉ giữ một `opt` cho ghi bản ghi ở chế độ đồng thời và một `ref` khởi tạo; header có khoảng trống riêng. `BenchmarkResult` xuất hiện tại thời điểm được tạo.
- [Activity diagram](activity-diagram.drawio): ba swimlane, initial/final, một quyết định với hai nhánh tuần tự/đồng thời, merge và ghi báo cáo. Các vòng lặp và chi tiết producer/consumer được gộp trong hành động xử lý để dễ đọc tổng thể.

Ký hiệu cơ bản đối chiếu [UML 2.5.1 của OMG](https://www.omg.org/spec/UML/2.5.1). Boundary/control/entity (BCE) là vai trò phân tích dùng để đọc sequence, không phải yêu cầu bắt buộc cho mọi lifeline trong UML hay annotation trong Java. Processor trên sequence đại diện phần xử lý bên trong, gồm producer/queue/consumer ở các mode đồng thời. `write(record)` đại diện lời gọi từ consumer và lặp cho các bản ghi; chi tiết thread, vòng lặp và poison pill được lược khỏi hình.

Sequence phân biệt đúng lời gọi và kết quả: `Runner.run()` và `Processor.process()` đều trả `void`; sau đó gọi `getResult()` riêng. Thời gian đo chỉ bao quanh `process()`. Hai mode tuần tự không tạo `ProcessedRecord` và không dùng/đóng RecordWriter.

Sơ đồ xử lý mô tả một lần chạy thành công, N > 0, không thêm validation/retry/cleanup mà source chưa có. QUEUE chờ bằng `join`; EXECUTOR dùng `shutdown` và `awaitTermination`; VIRTUAL dùng `Future.get`. Các getter/constructor và lớp phụ được lược khỏi class diagram để giữ hình dễ đọc. `LargeFileGenerator` là tiện ích sinh file thử, hiện không được gọi tự động từ `main`.

Lưu ý: mã hiện tại truyền đảo tổng dòng/từ trong cả ba processor đồng thời, nên báo cáo bị đảo hai số đếm. Sơ đồ có ghi chú điểm này; mã Java không được sửa.

Tái tạo bằng `python docs/concurrent/build_uml.py`. Bộ tạo kiểm tra XML, đầu mút đường nối, ngăn lớp, khổ trang và ký hiệu chính. Ba file được mở thử bằng bộ hiển thị diagrams.net để rà soát bố cục.
