# Sử dụng Python base image
FROM python:3.9

# Đặt thư mục làm việc trong container là /app
WORKDIR /app

# Copy riêng requirements.txt trước để giữ cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Sau đó mới copy toàn bộ code
COPY . .

# Expose cổng 8000
EXPOSE 8000

# Chạy ứng dụng FastAPI với Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]