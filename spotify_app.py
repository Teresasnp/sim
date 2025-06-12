import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(layout="wide")
st.title("Analisis Data Lagu Spotify")

# Sidebar Navigasi
st.sidebar.title("Navigasi")
halaman = st.sidebar.radio("Pilih bagian:", [
    "1. Menyiapkan Library",
    "2. Data Wrangling",
    "3. Assessing Data",
    "4. Cleaning Data",
    "5. EDA (Exploratory Data Analysis)",
    "6. Visualisasi & Penjelasan"
])

# Fungsi cleaning
def clean_data(df):
    df['Length (Duration)'] = pd.to_numeric(df['Length (Duration)'], errors='coerce')
    df['Year'] = df['Year'].fillna(0).astype(int)
    df['Length (Duration)'] = (df['Length (Duration)'] / 60).round(2)
    df['Speechiness'] = df['Speechiness'] / 100

    # Perbaikan manual
    df.loc[df['Title'] == 'Fix You', 'Year'] = 2005
    df.loc[df['Title'] == 'Miracle', 'Year'] = 2008
    df.loc[df['Title'].str.contains('7 Seconds', na=False), 'Year'] = 1994
    df.loc[df['Title'] == 'Echoes', 'Length (Duration)'] = 23.34
    df.loc[df['Title'].str.contains('Close to the Edge', na=False), 'Length (Duration)'] = 18.42
    df.loc[df['Title'].str.contains('Autobahn', na=False), 'Length (Duration)'] = 22.48
    df.loc[df['Title'] == 'Get Ready', 'Length (Duration)'] = 21.32

    # Kolom kategori tempo
    def tempo_category(bpm):
        if bpm < 90:
            return 'Slow'
        elif bpm <= 130:
            return 'Medium'
        else:
            return 'Fast'

    df['Tempo_Category'] = df['Beats Per Minute (BPM)'].apply(tempo_category)
    return df

uploaded_file = st.file_uploader("Unggah file CSV Spotify", type=["csv"])

if uploaded_file is not None:
    lagu_data = pd.read_csv(uploaded_file)
    lagu_data = clean_data(lagu_data)  # ← Cleaning otomatis

    # Halaman 1
    if halaman == "1. Menyiapkan Library":
        st.markdown("✅ **Library utama** seperti `pandas`, `numpy`, `seaborn`, `matplotlib`, `scipy`, dan `streamlit` telah diimpor untuk analisis.")

    # Halaman 2
    elif halaman == "2. Data Wrangling":
        st.subheader("📊 Tampilan Awal Dataset")
        st.write(lagu_data.head())
        st.write("Ukuran data:", lagu_data.shape)

    # Halaman 3
    elif halaman == "3. Assessing Data":
        st.subheader("🔍 Informasi Dataset")
        st.text(str(lagu_data.info()))
        st.subheader("🧩 Cek Nilai Kosong")
        st.write(lagu_data.isnull().sum())
        st.subheader("📌 Cek Duplikasi")
        st.write(lagu_data.duplicated().sum())

    # Halaman 4
    elif halaman == "4. Cleaning Data":
        st.subheader("🧹 Proses Cleaning Data")
        st.success("✅ Cleaning telah dilakukan otomatis saat file diunggah.")
        st.write(lagu_data.head())

    # Halaman 5
    elif halaman == "5. EDA (Exploratory Data Analysis)":
        st.subheader("📈 Deskripsi Statistik")
        st.dataframe(lagu_data.describe())

        st.subheader("🎵 Distribusi Genre Musik")
        genre_counts = lagu_data['Top Genre'].value_counts()
        st.bar_chart(genre_counts)

        st.subheader("⏱️ Distribusi Tempo (BPM)")
        fig, ax = plt.subplots()
        sns.histplot(lagu_data['Beats Per Minute (BPM)'], kde=True, ax=ax)
        st.pyplot(fig)

        st.subheader("⚡ Rata-rata Energy per Artis")
        st.write(lagu_data.groupby('Artist')['Energy'].mean().sort_values(ascending=False).head(10))

    # Halaman 6: Visualisasi Berdasarkan 10 Pertanyaan
    elif halaman == "6. Visualisasi & Penjelasan":
        st.subheader("🔟 Visualisasi Menjawab 10 Pertanyaan")

        st.subheader("1. Genre dengan Jumlah Lagu Terbanyak")
        st.bar_chart(lagu_data['Top Genre'].value_counts().head(10))

        st.subheader("2. Distribusi Kategori Tempo")
        st.bar_chart(lagu_data['Tempo_Category'].value_counts())

        st.subheader("3. Artis dengan Rata-rata Energy Tertinggi")
        st.write(lagu_data.groupby('Artist')['Energy'].mean().sort_values(ascending=False).head(5))

        st.subheader("4. Artis dengan Rata-rata Danceability dan Popularitas Tertinggi")
        st.write(lagu_data.groupby('Artist')[['Danceability', 'Popularity']].mean().sort_values(by='Danceability', ascending=False).head(5))

        st.subheader("5. Genre dengan Tempo Tertinggi")
        st.write(lagu_data.groupby('Top Genre')['Beats Per Minute (BPM)'].mean().sort_values(ascending=False).head(5))

        st.subheader("6. Genre yang Paling Sering Muncul")
        st.write(lagu_data['Top Genre'].value_counts().head(5))

        st.subheader("7. Artis dengan Lagu Terbanyak dan Popularitas Tertinggi")
        populer = lagu_data.groupby('Artist').agg({'Title':'count','Popularity':'mean'}).sort_values(by='Title', ascending=False).head(5)
        st.dataframe(populer.rename(columns={'Title':'Jumlah Lagu'}))

        st.subheader("8. Penyanyi dengan Rata-rata Durasi Lagu Terpanjang")
        st.write(lagu_data.groupby('Artist')['Length (Duration)'].mean().sort_values(ascending=False).head(5))

        st.subheader("9. Tren Popularitas Lagu dari Tahun ke Tahun")
        pop_trend = lagu_data.groupby('Year')['Popularity'].mean()
        fig, ax = plt.subplots()
        pop_trend.plot(kind='line', ax=ax)
        ax.set_title("Tren Popularitas per Tahun")
        st.pyplot(fig)

        st.subheader("10. Distribusi Lagu Berdasarkan Tempo Category")
        fig, ax = plt.subplots()
        sns.countplot(x='Tempo_Category', data=lagu_data, ax=ax)
        st.pyplot(fig)
else:
    st.info("📂 Silakan unggah file CSV untuk memulai analisis.")
