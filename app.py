import streamlit as st
from PIL import Image
import requests
import base64
import json
import io

# --- Konfigurasi Halaman dan Styling ---
st.set_page_config(
    page_title="Gemini OCR",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gunakan CSS kustom untuk memberikan tampilan yang lebih mewah
st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #4A90E2;
            text-shadow: 2px 2px 4px #000000;
            text-align: center;
        }
        .subheader {
            font-size: 1.5rem;
            color: #555555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stButton>button {
            color: white;
            background-color: #4A90E2;
            border-radius: 10px;
            border: none;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            font-size: 1.2rem;
            padding: 10px 20px;
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #5A9BE0;
            transform: scale(1.05);
            box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
        }
        .stExpander {
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

# Variabel untuk API Key (akan diisi secara otomatis oleh Canvas)
API_KEY = "" # Biarkan kosong, akan diisi saat dijalankan

# --- Sidebar untuk Unggahan dan Pengaturan ---
with st.sidebar:
    st.title("✨RNJ  Gemini OCR App")
    st.markdown("---")
    st.header("Unggah Struk")
    uploaded_file = st.file_uploader(
        "Pilih gambar struk",
        type=["png", "jpg", "jpeg"]
    )
    st.markdown("---")
    st.header("Pengaturan OCR")
    # Anda bisa menambahkan lebih banyak opsi di sini, misal:
    # `st.checkbox("Ekstrak Harga Saja")`
    st.info("Opsi tambahan akan segera hadir!")

# --- Konten Utama Aplikasi ---
st.markdown("<h1 class='main-header'>OCR Struk Harga dengan Gemini API</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Unggah gambar struk Anda di sidebar untuk memulai analisis.</p>", unsafe_allow_html=True)

if uploaded_file is not None:
    # Gunakan layout kolom untuk tata letak yang lebih baik
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Gambar yang Diunggah")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True, output_format='PNG')

    with col2:
        st.header("Analisis Teks")
        
        # Tombol untuk memicu analisis
        if st.button("Jalankan OCR"):
            with st.spinner("Mengekstrak teks..."):
                try:
                    # Konversi gambar menjadi base64 untuk dikirim ke API
                    with io.BytesIO() as output:
                        image.save(output, format=image.format)
                        image_bytes = output.getvalue()
                        base64_image = base64.b64encode(image_bytes).decode('utf-8')
                        
                    # Prompt yang akan dikirim ke Gemini
                    prompt = "Ekstrak semua teks yang terlihat dari gambar struk harga ini. Fokus pada nama produk, jumlah, dan harga, dan sajikan hasilnya dengan terstruktur."

                    # Payload untuk Gemini API
                    payload = {
                        "contents": [
                            {
                                "parts": [
                                    {"text": prompt},
                                    {
                                        "inlineData": {
                                            "mimeType": uploaded_file.type,
                                            "data": base64_image
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                    
                    # Konfigurasi API
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
                    headers = {"Content-Type": "application/json"}
                    
                    # Kirim permintaan ke Gemini API
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    response.raise_for_status() # Memicu exception jika respons HTTP error
                    
                    result = response.json()
                    
                    # Parsing hasil respons
                    text = result.get('candidates')[0].get('content').get('parts')[0].get('text')
                    
                    if text:
                        st.success("Teks berhasil diekstrak!")
                        # Tampilkan hasil di expander untuk tampilan yang lebih rapi
                        with st.expander("Lihat Hasil OCR", expanded=True):
                            st.markdown(f"```\n{text}\n```")
                    else:
                        st.warning("Tidak ada teks yang berhasil diekstrak.")

                except requests.exceptions.RequestException as e:
                    st.error(f"Terjadi kesalahan saat terhubung ke Gemini API: {e}")
                    st.info("Pastikan Anda memiliki koneksi internet dan API Key yang valid.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses data: {e}")
else:
    st.info("Unggah gambar struk Anda di sidebar sebelah kiri untuk memulai.")
