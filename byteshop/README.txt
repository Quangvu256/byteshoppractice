============================================================
           HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY DỰ ÁN
     (The Local Data Stack: E-commerce Analytics with dbt & DuckDB)
============================================================

Mô tả: Hướng dẫn này cung cấp các bước để cài đặt và chạy toàn bộ
đường ống dữ liệu phân tích hành vi người dùng TMĐT trên máy tính cá nhân.

------------------------------------------------------------
I. YÊU CẦU MÔI TRƯỜNG (PREREQUISITES)
------------------------------------------------------------

Hãy chắc chắn bạn đã cài đặt các phần mềm sau trên máy tính:

1. Python (phiên bản 3.8 trở lên)
2. Docker Desktop (phải đang ở trạng thái "Running")
3. Một trình soạn thảo code như VS Code.


------------------------------------------------------------
II. CÁC BƯỚC CÀI ĐẶT VÀ THỰC THI
------------------------------------------------------------

Thực hiện các lệnh sau từ cửa sổ Terminal (PowerShell) tại thư mục gốc của dự án.

---
**BƯỚC 1: CÀI ĐẶT CÁC THƯ VIỆN PYTHON**
---

Dự án sử dụng một số thư viện. Chạy lệnh sau để cài đặt tất cả:

pip install faker mage-ai pandas duckdb dbt-duckdb


---
**BƯỚC 2: TẠO DỮ LIỆU THÔ (RAW DATA)**
---

Chạy script để tạo ra file dữ liệu mẫu.

python generate_events_single_file.py

* Kết quả mong đợi: Một thư mục mới `generated_events_single` được tạo ra,
    chứa file `all_events.jsonl`.


---
**BƯỚC 3: CHẠY PIPELINE ETL (EXTRACT-TRANSFORM-LOAD) BẰNG MAGE**
---

1.  Khởi động Mage. Lệnh này sẽ chạy một trang web trên máy của bạn.

    mage start mage_project

2.  Mở trình duyệt web và truy cập: http://localhost:6789

3.  Tìm pipeline có tên `local_events_to_duckdb` và nhấn nút "Run pipeline once"
    để thực thi.

* Kết quả mong đợi: Một thư mục `data` được tạo ra, chứa file "nhà kho"
    là `byteshop.db`. Bảng `raw_events` bên trong file này sẽ chứa dữ liệu.


---
**BƯỚC 4: CHẠY QUÁ TRÌNH BIẾN ĐỔI DỮ LIỆU (TRANSFORMATION) BẰNG DBT**
---

1.  Trong Terminal, di chuyển vào thư mục của dbt:

    cd dbt_byteshop

2.  Kiểm tra kết nối của dbt tới "nhà kho":

    dbt debug

    (Tất cả các mục kiểm tra phải báo "OK" màu xanh lá).

3.  Ra lệnh cho dbt "xây dựng" các mô hình dữ liệu đã được định nghĩa:

    dbt run

4.  Sau khi chạy xong, quay trở lại thư mục gốc:

    cd ..

* Kết quả mong đợi: Các bảng/view mới (như `dm_product_funnel`) được tạo ra
    bên trong file `data/byteshop.db`.


---
**BƯỚC 5: KHỞI ĐỘNG BẢNG ĐIỀU KHIỂN (DASHBOARD) VỚI METABASE**
---

1.  Dừng và xóa các container Metabase cũ có thể đang chạy (nếu có):

    docker stop metabase
    docker rm metabase

2.  Chạy lệnh sau để khởi động Metabase. Lệnh này sẽ "gắn" thư mục `data`
    của bạn vào bên trong Metabase.

    (Lưu ý: Biến `%cd%` sẽ tự động lấy đường dẫn thư mục hiện tại của bạn)

    docker run -d -p 3000:3000 -v "%cd%\data:/metabase-data" --name metabase metabase/metabase

3.  Mở trình duyệt và truy cập: http://localhost:3000
    (Có thể mất 1-2 phút để Metabase khởi động xong).

4.  Thực hiện các bước cài đặt ban đầu cho Metabase. Khi kết nối tới database,
    sử dụng các thông tin sau:
    -   Loại Database: DuckDB
    -   Đường dẫn file database: /metabase-data/byteshop.db


------------------------------------------------------------
III. KẾT QUẢ CUỐI CÙNG
------------------------------------------------------------

Sau khi hoàn thành tất cả các bước, bạn có thể đăng nhập vào Metabase,
khám phá dữ liệu từ bảng `dm_product_funnel`, và xây dựng các biểu đồ
phân tích như biểu đồ phễu, top sản phẩm...

------------------------------------------------------------