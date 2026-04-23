# 🚲 Bike Sharing Analysis Dashboard

Proyek ini merupakan bagian dari tugas analisis data untuk mengeksplorasi pola penyewaan sepeda pada dataset **Bike Sharing**. Dashboard ini dibangun menggunakan **Streamlit** untuk memvisualisasikan wawasan (insights) utama terkait tren waktu dan pengaruh cuaca terhadap jumlah penyewaan.

## 📊 Pertanyaan Bisnis
1. **Pola Jam Operasional:** Bagaimana pola jumlah penyewaan sepeda berdasarkan jam dalam satu hari pada tahun 2011–2012 dan kapan waktu dengan tingkat penyewaan tertinggi terjadi?
2. **Dampak Cuaca:** Bagaimana pengaruh kondisi cuaca terhadap rata-rata jumlah penyewaan sepeda per hari selama periode 2011–2012?

## 🚀 Fitur Dashboard
- **Metrik Utama:** Menampilkan total penyewa, rata-rata harian, serta nilai puncak penyewaan.
- **Filter Interaktif:** Pengguna dapat memfilter data berdasarkan rentang tanggal dan kondisi cuaca di sidebar.
- **Visualisasi Tren:** Grafik garis dan batang untuk melihat pola fluktuasi per jam.
- **Analisis Lanjutan:** Manual clustering berdasarkan segmen waktu (Rush Hours, Business Hours, Evening Leisure, Rest Time) untuk melihat perilaku pengguna secara makro.

## 📂 Struktur Direktori
```text
.
├── dashboard/
│   ├── dashboard.py       # File utama aplikasi Streamlit
│   └── main_data.csv      # Dataset hasil merge yang sudah dibersihkan
├── data/
│   ├── day.csv            # Dataset harian mentah
│   └── hour.csv           # Dataset per jam mentah
├── notebook.ipynb         # Proses analisis data (EDA, Cleaning, Visualisasi)
├── requirements.txt       # Daftar pustaka Python yang dibutuhkan
└── README.md              # Panduan proyek

## Setup Environment - Anaconda
conda create --name bike-sharing-env python=3.13.5
conda activate bike-sharing-env
pip install -r requirements.txt

Run steamlit app
git clone https://bike-sharing-dicoding-dindaradityaswari.streamlit.app/ 
cd bike-sharing-dicoding 
Masuk ke folder dashboard cd dashboard
streamlit run dashboard.py
