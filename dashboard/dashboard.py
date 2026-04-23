import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import os

# --- FORMAT ANGKA INDONESIA ---
def fmt(value, decimals=0):
    """Format angka dengan pemisah ribuan titik dan desimal koma (ID locale)."""
    formatted = f"{value:,.{decimals}f}"          # contoh: 1,234.56
    formatted = formatted.replace(",", "X")        # 1X234.56
    formatted = formatted.replace(".", ",")        # 1X234,56
    formatted = formatted.replace("X", ".")        # 1.234,56
    return formatted

# --- CONFIG & STYLE ---
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "main_data.csv")
    df = pd.read_csv(path)
    df['dteday'] = pd.to_datetime(df['dteday'])

    df['weather_code'] = pd.to_numeric(df['weather_code'], errors='coerce').fillna(1).astype(int)

    weather_map = {
        1: 'Clear',
        2: 'Misty/Cloudy',
        3: 'Light Rain/Snow',
        4: 'Heavy Rain'
    }
    df['weather_label'] = df['weather_code'].map(weather_map).fillna('Unknown')

    return df

df = load_data()

# --- SIDEBAR FILTER ---
with st.sidebar:
    st.title("🚲 Bike Sharing Analytics")
    st.header("Filter Data")

    min_date, max_date = df["dteday"].min(), df["dteday"].max()
    start_date, end_date = st.date_input("Rentang Waktu", value=[min_date, max_date])

    available_weather = sorted(df['weather_label'].unique().tolist())
    selected_weather = st.multiselect(
        "Pilih Cuaca",
        options=available_weather,
        default=available_weather
    )

# --- FILTER DATA ---
main_df = df[
    (df['dteday'] >= pd.to_datetime(start_date)) &
    (df['dteday'] <= pd.to_datetime(end_date)) &
    (df['weather_label'].isin(selected_weather))
]

# --- HEADER & METRICS ---
st.title("Dashboard Analisis Penyewaan Sepeda")

if not selected_weather:
    st.warning("⚠️ Silakan pilih minimal satu kondisi cuaca di sidebar.")
    st.stop()

if main_df.empty:
    st.warning("⚠️ Tidak ada data untuk filter yang dipilih. Coba ubah rentang tanggal atau kondisi cuaca.")
    st.stop()

weather_text = ", ".join(map(str, selected_weather))
st.markdown(f"Statistik untuk kondisi: **{weather_text}**")
st.markdown(f"Statistik untuk periode: **{start_date}** s/d **{end_date}**")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penyewa", fmt(main_df['cnt_hour'].sum()))
with col2:
    st.metric("Avg Harian", fmt(main_df.groupby('dteday')['cnt_hour'].sum().mean()))
with col3:
    st.metric("Peak Rentals", fmt(main_df['cnt_hour'].max()))
with col4:
    st.metric("Min Rentals", fmt(main_df['cnt_hour'].min()))

st.markdown("---")

# --- PERTANYAAN 1: TREND PER JAM ---
st.subheader("1️⃣ Tren Penyewaan Berdasarkan Jam Operasional")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Line Chart: Pola Fluktuasi per Jam**")
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_avg = main_df.groupby('hr')['cnt_hour'].mean().reset_index()
    sns.lineplot(data=hourly_avg, x='hr', y='cnt_hour', marker='o', color='#B32A19', ax=ax)
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)
    plt.close()

with col_b:
    st.markdown("**Bar Chart: Jam Sibuk (Top 5 Peak Hours)**")
    fig, ax = plt.subplots(figsize=(10, 6))
    top5_hours = hourly_avg.nlargest(5, 'cnt_hour')['hr'].tolist()
    colors = ['#E53935' if x in top5_hours else '#CFD8DC' for x in hourly_avg['hr']]
    bars = sns.barplot(data=hourly_avg, x='hr', y='cnt_hour', palette=colors, ax=ax)
    for bar in bars.patches:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                fmt(height, 0),           # ← format ID, tanpa desimal
                ha='center', va='bottom', fontsize=7, fontweight='bold'
            )
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)
    plt.close()

# --- PERTANYAAN 2: DAMPAK CUACA ---
st.markdown("---")
st.subheader("2️⃣ Dampak Kondisi Cuaca Terhadap Penyewaan")
col_c, col_d = st.columns(2)

weather_code_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
existing_codes = sorted(main_df['weather_code'].unique().tolist())
x_labels = [weather_code_labels.get(c, str(c)) for c in existing_codes]

with col_c:
    st.markdown("**Bar Chart: Rata-rata per Kategori Cuaca**")
    fig, ax = plt.subplots(figsize=(10, 6))
    weather_avg = main_df.groupby('weather_code')['cnt_day'].mean().reset_index()
    colors = ['#B32A19', '#C96E68', '#D89D9A']
    sns.barplot(data=weather_avg, x='weather_code', y='cnt_day', palette=colors, ax=ax)
    for bar in ax.patches:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 10,
                fmt(height, 1),           # ← format ID, 1 desimal pakai koma
                ha='center', va='bottom', fontsize=10, fontweight='bold'
            )
    ax.set_xticks(range(len(existing_codes)))
    ax.set_xticklabels(x_labels)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Harian")
    st.pyplot(fig)
    plt.close()

with col_d:
    st.markdown("**Box Plot: Variasi dan Outlier Data**")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#B32A19', '#C96E68', '#D89D9A']
    sns.boxplot(data=main_df, x='weather_code', y='cnt_day', palette=colors, ax=ax)
    ax.set_xticks(range(len(existing_codes)))
    ax.set_xticklabels(x_labels)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Jumlah Penyewaan Harian")
    st.pyplot(fig)
    plt.close()

# --- ANALISIS LANJUTAN: CLUSTERING ---
st.markdown("---")
st.subheader("🎯 Analisis Lanjutan: Manual Clustering Berdasarkan Waktu")
st.markdown("Mengelompokkan aktivitas berdasarkan segmen waktu produktif.")

fig, ax = plt.subplots(figsize=(12, 5))
segment_data = main_df.groupby('time_segment')['cnt_hour'].mean().sort_values(ascending=False).reset_index()
colors = ['#B32A19', '#C96E68', '#D89D9A', '#FFE1DE']
sns.barplot(data=segment_data, x='cnt_hour', y='time_segment', palette=colors, ax=ax)

for i, v in enumerate(segment_data['cnt_hour']):
    ax.text(v + 3, i, fmt(v, 1), va='center', fontweight='bold')  # ← format ID

ax.set_xlabel("Rata-rata Jumlah Penyewaan")
ax.set_ylabel("Segmen Waktu")
st.pyplot(fig)
plt.close()

# --- FOOTER ---
st.markdown("---")
st.caption("Copyright © 2026 | Bike Sharing Analysis Project - Made Dinda Radityaswari")