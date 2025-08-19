FROM python:3.11-slim

WORKDIR /app

# تثبيت curl و Nodejs حديث + pnpm
RUN apt-get update && apt-get install -y curl build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g pnpm && \
    rm -rf /var/lib/apt/lists/*

# تثبيت باكدجات Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# ===== Build Frontend =====
WORKDIR /app/gui/ohunter-ui
RUN pnpm install && pnpm run build

# نقل الـ build إلى static folder
RUN mkdir -p /app/core/static && cp -r build/* /app/core/static/

# رجوع لمجلد الباك إند
WORKDIR /app

# تعيين متغيرات البيئة
ENV PYTHONPATH=/app:/app/core:/app/modules
EXPOSE $PORT

# تشغيل السيرفر
CMD ["python", "core/app.py"]
