import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

"""
utils.py
Kumpulan fungsi penunjang untuk proyek analisis sentimen cryptocurrency.

Fungsi yang tersedia:
1. load_data            -> memuat dan membersihkan dataset mentah
2. hitung_korelasi_pearson   -> menghitung korelasi Pearson antara dua variabel
3. korelasi_per_kelompok -> menghitung korelasi Pearson per kelompok (misalnya per koin)
4. buat_grafik_dual_axis -> membuat grafik dual-axis (harga vs sentimen) terhadap waktu
"""



def load_data(filepath, kolom_waktu_kandidat=("DateTime", "Date"), koin=None, kolom_koin="Coin"):
    """
    Memuat dataset mentah dari file CSV.

    Parameter:
        filepath (str): path menuju file CSV.
        kolom_waktu_kandidat (tuple): nama kolom waktu yang dicoba secara berurutan,
            karena beberapa dataset menamai kolom waktu sebagai 'DateTime' atau 'Date'.
        koin (str atau None): jika diisi, data akan difilter hanya untuk koin tersebut
            (berlaku jika dataset memiliki kolom identitas koin).
        kolom_koin (str): nama kolom yang menyimpan identitas koin/aset.

    Return:
        pandas.DataFrame yang sudah terurut berdasarkan waktu, dengan kolom waktu
        yang sudah diseragamkan namanya menjadi 'DateTime'.
    """
    df = pd.read_csv(filepath)

    # Menyeragamkan nama kolom waktu menjadi 'DateTime'
    kolom_waktu_ditemukan = None
    for nama_kolom in kolom_waktu_kandidat:
        if nama_kolom in df.columns:
            kolom_waktu_ditemukan = nama_kolom
            break

    if kolom_waktu_ditemukan is None:
        raise ValueError(
            f"Tidak ditemukan kolom waktu. Kolom yang dicoba: {str(kolom_waktu_kandidat)}"
        )

    df = df.rename(columns={kolom_waktu_ditemukan: "DateTime"})
    df["DateTime"] = pd.to_datetime(df["DateTime"])

    # Filter berdasarkan koin tertentu apabila diminta dan kolomnya tersedia
    if koin is not None and kolom_koin in df.columns:
        df = df[df[kolom_koin] == koin].copy()

    # Menghapus baris dengan nilai kosong pada kolom numerik utama
    kolom_numerik = df.select_dtypes(include="number").columns
    df = df.dropna(subset=kolom_numerik)

    df = df.sort_values("DateTime").reset_index(drop=True)
    return df


def hitung_korelasi_pearson(df, kolom_x="Sentiment_Score", kolom_y="Volatility_Index"):
    """
    Menghitung koefisien korelasi Pearson antara dua kolom numerik.

    Parameter:
        df (pandas.DataFrame): data yang akan dianalisis.
        kolom_x (str): nama kolom variabel pertama.
        kolom_y (str): nama kolom variabel kedua.

    Return:
        dict berisi:
            r            -> koefisien korelasi Pearson
            p_value      -> nilai p dari uji korelasi
            n            -> jumlah observasi yang digunakan
            interpretasi -> keterangan kekuatan hubungan dalam bahasa sederhana
    """
    data_bersih = df[[kolom_x, kolom_y]].dropna()
    r, p_value = stats.pearsonr(data_bersih[kolom_x], data_bersih[kolom_y])

    # Interpretasi kekuatan korelasi berdasarkan nilai absolut r
    r_absolut = abs(r)
    if r_absolut < 0.10:
        kekuatan = "sangat lemah / tidak ada korelasi yang berarti"
    elif r_absolut < 0.30:
        kekuatan = "lemah"
    elif r_absolut < 0.50:
        kekuatan = "sedang"
    elif r_absolut < 0.70:
        kekuatan = "kuat"
    else:
        kekuatan = "sangat kuat"

    signifikan = "signifikan (p < 0.05)" if p_value < 0.05 else "tidak signifikan (p >= 0.05)"

    arah = "positif" if r > 0 else "negatif"
    interpretasi = f"Hubungan antara {kolom_x} dan {kolom_y} tergolong {kekuatan} dan berarah {arah}, serta secara statistik {signifikan}."

    return {
        "r": r,
        "p_value": p_value,
        "n": len(data_bersih),
        "interpretasi": interpretasi,
    }


def korelasi_per_kelompok(df, kolom_grup="Coin", kolom_x="Sentiment_Score", kolom_y="Volatility_Index"):
    """
    Menghitung korelasi Pearson secara terpisah untuk setiap kelompok/kategori.
    Fungsi ini berguna jika dataset berisi lebih dari satu aset (misalnya beberapa
    cryptocurrency sekaligus), sehingga korelasi tidak bias akibat perbedaan
    karakteristik antar aset.

    Parameter:
        df (pandas.DataFrame): data yang akan dianalisis.
        kolom_grup (str): nama kolom yang menjadi dasar pengelompokan.
        kolom_x (str): nama kolom variabel pertama.
        kolom_y (str): nama kolom variabel kedua.

    Return:
        pandas.DataFrame berisi ringkasan korelasi untuk tiap kelompok, atau
        None apabila kolom_grup tidak tersedia pada dataset.
    """
    if kolom_grup not in df.columns:
        return None

    daftar_hasil = []
    for nama_grup, data_grup in df.groupby(kolom_grup):
        hasil = hitung_korelasi_pearson(data_grup, kolom_x, kolom_y)
        daftar_hasil.append(
            {
                kolom_grup: nama_grup,
                "n": hasil["n"],
                "r": hasil["r"],
                "p_value": hasil["p_value"],
            }
        )

    return pd.DataFrame(daftar_hasil).sort_values("r", ascending=False).reset_index(drop=True)


def buat_grafik_dual_axis(
    df,
    kolom_waktu="DateTime",
    kolom_harga="Price_USD",
    kolom_sentimen="Sentiment_Score",
    output_path="grafik_output.png",
    judul="Perbandingan Harga dan Sentimen Pasar",
):
    """
    Membuat grafik dual-axis yang menampilkan pergerakan harga (sumbu kiri)
    dan sentimen pasar (sumbu kanan) terhadap waktu, kemudian menyimpannya
    sebagai file gambar.

    Parameter:
        df (pandas.DataFrame): data yang akan divisualisasikan, harus sudah
            terurut berdasarkan waktu.
        kolom_waktu (str): nama kolom waktu.
        kolom_harga (str): nama kolom harga.
        kolom_sentimen (str): nama kolom skor sentimen.
        output_path (str): path penyimpanan file gambar.
        judul (str): judul grafik.
    """
    fig, sumbu_harga = plt.subplots(figsize=(11, 5))

    # Sumbu kiri: harga
    warna_harga = "tab:blue"
    sumbu_harga.set_xlabel("Waktu")
    sumbu_harga.set_ylabel("Harga (USD)", color=warna_harga)
    sumbu_harga.plot(df[kolom_waktu], df[kolom_harga], color=warna_harga, linewidth=1.5, label="Harga (USD)")
    sumbu_harga.tick_params(axis="y", labelcolor=warna_harga)

    # Sumbu kanan: sentimen
    sumbu_sentimen = sumbu_harga.twinx()
    warna_sentimen = "tab:red"
    sumbu_sentimen.set_ylabel("Sentiment Score", color=warna_sentimen)
    sumbu_sentimen.plot(
        df[kolom_waktu], df[kolom_sentimen], color=warna_sentimen, linewidth=1.0, alpha=0.7, label="Sentiment Score"
    )
    sumbu_sentimen.tick_params(axis="y", labelcolor=warna_sentimen)

    fig.suptitle(judul)
    fig.autofmt_xdate()
    fig.tight_layout()

    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    
def scatter_plot(df, kolom_x="Sentiment_Score", kolom_y="Volatility_Index", output_path="scatter_plot.png"):
    """
    Membuat scatter plot untuk memvisualisasikan hubungan antara dua variabel.

    Parameter:
        df (pandas.DataFrame): data yang akan divisualisasikan.
        kolom_x (str): nama kolom variabel pada sumbu x.
        kolom_y (str): nama kolom variabel pada sumbu y.
        output_path (str): path penyimpanan file gambar.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(df[kolom_x], df[kolom_y], alpha=0.5)
    plt.title(f"Scatter Plot: {kolom_x} vs {kolom_y}")
    plt.xlabel(kolom_x)
    plt.ylabel(kolom_y)
    plt.grid(True)
    plt.savefig(output_path, dpi=150)
    plt.close()

    
def buat_heatmap_korelasi(df, kolom_numerik, output_path="heatmap_korelasi.png"):
    """
    Membuat Heatmap korelasi antar berbagai variabel numerik.
    """
    korelasi = df[kolom_numerik].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(korelasi, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
    plt.title("Heatmap Korelasi Variabel Pasar Kripto")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

def buat_cross_correlation_plot(df, koin, kolom_sentimen="Sentiment_Score", kolom_target="Volatility_Index", max_lag=7, output_path="cross_corr.png"):
    """
    Membuat Cross-Correlation Plot untuk melihat efek jeda waktu (time-lag)
    antara Hype (Sentimen) dan Volatilitas untuk koin tertentu.
    """
    # Pastikan data diurutkan berdasarkan waktu
    df_koin = df[df["Coin"] == koin].copy()
    df_koin = df_koin.sort_values("DateTime")
    
    lags = range(-max_lag, max_lag + 1)
    korelasi_lags = []
    
    for lag in lags:
        # shift(-lag) berarti menggeser target ke belakang/depan sebanyak 'lag' hari
        corr = df_koin[kolom_sentimen].corr(df_koin[kolom_target].shift(-lag))
        korelasi_lags.append(corr)
        
    plt.figure(figsize=(10, 6))
    # Gunakan marker untuk titik-titik lag
    plt.stem(lags, korelasi_lags, basefmt=" ")
    plt.axhline(0, color='black', linewidth=1)
    
    plt.title(f"Cross-Correlation: Hype vs Volatilitas ({koin})")
    plt.xlabel("Lag (Hari)\n<-- Sentimen Mengikuti Volatilitas | Sentimen Mendahului Volatilitas -->")
    plt.ylabel("Korelasi Pearson (r)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

def hitung_time_lagged_correlation(df, koin, kolom_sentimen="Sentiment_Score", kolom_target="Volatility_Index", max_lag=7):
    """
    Fungsi untuk menghasilkan teks perhitungan korelasi dengan time-lag (T+n).
    Berguna untuk dimasukkan secara otomatis ke hasil_analisis.txt
    """
    df_koin = df[df["Coin"] == koin].copy()
    df_koin = df_koin.sort_values("DateTime")
    
    hasil_teks = f"Time-Lagged Correlation untuk {koin} ({kolom_sentimen} ke {kolom_target}):\n"
    for lag in range(1, max_lag + 1):
        corr = df_koin[kolom_sentimen].corr(df_koin[kolom_target].shift(-lag))
        hasil_teks += f"- Pengaruh Hype hari ini terhadap Volatilitas {lag} hari ke depan (Lag +{lag}): r = {corr:.4f}\n"
    
    return hasil_teks