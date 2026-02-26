# Air Quality Data Pipeline
> mini ETL Pipeline: EXTRACT - request.get, TRANSFORM - parse JSON + convert datetime, LOAD - insert DB


---

# Yêu Cầu Cài Đặt

Trước khi chạy project, cần cài:

- Python 3.11+
- Docker
- Docker Compose
- Git

---


# Cấu Hình Biến Môi Trường

Tạo file `.env` ở thư mục gốc với nội dung:


API_KEY=your_api_key_here
DB_HOST=db
DB_NAME=air_quality
DB_USER=
DB_PASSWORD=
DB_PORT=5432


---

# Chạy Project Bằng Docker (Khuyến Nghị)

## Bước 1: Build và chạy container
docker-compose up --build

Lệnh này sẽ:

- Khởi động container PostgreSQL
- Khởi động container ứng dụng Python
- Tự động kết nối app với database

---

## Bước 2: Kiểm tra container đang chạy
docker ps

Bạn sẽ thấy:

- air_quality_app
- air_quality_db

---

## Bước 3: Dừng project
docker-compose down


---

# Tạo Database Thủ Công (Nếu Không Dùng Docker Compose)

Chạy PostgreSQL container:
docker run --name air_quality_db
-e POSTGRES_USER=
-e POSTGRES_PASSWORD=
-e POSTGRES_DB=air_quality
-p 5432:5432
-d postgres


---

# Chạy Local Không Dùng Docker

## Bước 1: Tạo môi trường ảo
python -m venv venv


## Bước 2: Kích hoạt môi trường

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

## Bước 3: Cài thư viện
pip install -r requirements.txt

## Bước 4: Chạy ứng dụng
python app/main.py


---

# Quy Trình Git

Khởi tạo repository:
git init

Thêm file:
git add .

Commit:
git commit -m "Initial commit"

Push bằng SSH:
git push -u origin main

>Luôn sử dụng SSH thay vì HTTPS để tránh lỗi 403.

---

# Giải Thích Kiến Trúc

## main.py
- Điểm bắt đầu của ứng dụng
- Điều phối việc chạy chương trình

## config.py
- Load biến môi trường từ `.env`
- Tách cấu hình khỏi logic
- Đảm bảo bảo mật

## services/
- Chứa business logic
- Gọi API
- Xử lý dữ liệu trước khi lưu vào database

