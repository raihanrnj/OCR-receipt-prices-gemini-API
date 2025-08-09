# Gunakan image Python yang lebih ringan
FROM python:3.9-slim

# Tetapkan direktori kerja
WORKDIR /app

# Instal dependensi sistem yang diperlukan (misalnya untuk requests atau PIL)
# Dalam kasus ini, tidak ada dependensi sistem khusus untuk Gemini API.
# Cukup pastikan sistem dasarnya bersih.
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

# Salin file requirements.txt dan instal dependensi Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file source code dari direktori lokal ke dalam image
COPY . .

# Paparkan port 8501, port default Streamlit
EXPOSE 8501

# Jalankan aplikasi Streamlit
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]
