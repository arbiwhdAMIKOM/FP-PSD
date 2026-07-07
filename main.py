import src.utils

"""
main.py
File eksekusi utama proyek akhir ST406 - Analisis Sentimen Cryptocurrency.

Alur program:
1. Memuat dataset mentah dari folder dataset/
2. Menghitung korelasi Pearson antara Sentiment_Score dan Volatility_Index
3. Menghitung korelasi tersebut per koin (karena dataset berisi beberapa aset)
4. Menyimpan ringkasan hasil ke hasil_analisis.txt
5. Membuat dan menyimpan grafik (harga vs sentimen) ke grafik_output.png
"""


# Konfigurasi path
DATASET_PATH = "/Users/arbiwhd/Kuliah/UAS_GENAP/PSD/proyek_akhir_ST406/Dataset/crypto_market_data_2026.csv"
OUTPUT_TXT = "/Users/arbiwhd/Kuliah/UAS_GENAP/PSD/proyek_akhir_ST406/hasil_txt/hasil_analisis.txt"
OUTPUT_PNG = "grafik_output.png"

# Koin yang dipakai sebagai contoh visualisasi deret waktu (harga vs sentimen)
KOIN_UNTUK_GRAFIK = "Bitcoin"


def main():
    # 1. Memuat data mentah
    df = src.utils.load_data(DATASET_PATH)
    print("Dataset berhasil dimuat. Jumlah baris:", len(df))

    # 2. Korelasi Pearson secara keseluruhan (seluruh baris digabung)
    hasil_keseluruhan = src.utils.hitung_korelasi_pearson(
        df, kolom_x="Sentiment_Score", kolom_y="Volatility_Index"
    )

    # 3. Korelasi Pearson per koin, karena menggabung beberapa aset yang berbeda
    #    skala harga dan karakteristiknya dapat membuat korelasi keseluruhan kurang representatif.
    tabel_per_koin = src.utils.korelasi_per_kelompok(
        df, kolom_grup="Coin", kolom_x="Sentiment_Score", kolom_y="Volatility_Index"
    )

    # 4. Menulis ringkasan hasil ke file teks
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("RINGKASAN ANALISIS SENTIMEN CRYPTOCURRENCY\n")
        f.write("Proyek Akhir Sains Data - ST406\n")
        f.write("=" * 50 + "\n\n")

        f.write("1. INFORMASI DATASET\n")
        f.write("-" * 50 + "\n")
        f.write("Jumlah baris data   : %d\n" % len(df))
        f.write("Rentang waktu        : %s s.d. %s\n" % (
            df["DateTime"].min().date(), df["DateTime"].max().date()
        ))
        if "Coin" in df.columns:
            f.write("Aset yang tercakup   : %s\n" % ", ".join(sorted(df["Coin"].unique())))
        f.write("\n")

        f.write("2. KORELASI PEARSON KESELURUHAN\n")
        f.write("-" * 50 + "\n")
        f.write("Variabel yang diuji  : Sentiment_Score vs Volatility_Index\n")
        f.write("Jumlah observasi (n) : %d\n" % hasil_keseluruhan["n"])
        f.write("Koefisien korelasi r : %.4f\n" % hasil_keseluruhan["r"])
        f.write("P-value              : %.4f\n" % hasil_keseluruhan["p_value"])
        f.write("Interpretasi         : %s\n\n" % hasil_keseluruhan["interpretasi"])

        if tabel_per_koin is not None:
            f.write("3. KORELASI PEARSON PER KOIN\n")
            f.write("-" * 50 + "\n")
            f.write("%-12s %-8s %-10s %-10s\n" % ("Koin", "n", "r", "p_value"))
            for _, baris in tabel_per_koin.iterrows():
                f.write(
                    "%-12s %-8d %-10.4f %-10.4f\n"
                    % (baris["Coin"], baris["n"], baris["r"], baris["p_value"])
                )
            f.write("\n")

        f.write("4. CATATAN\n")
        f.write("-" * 50 + "\n")
        f.write(
            "Nilai r mendekati 0 menunjukkan tidak ada hubungan linear yang jelas\n"
            "antara Sentiment_Score dan Volatility_Index pada data ini. P-value >= 0.05\n"
            "berarti hubungan tersebut tidak signifikan secara statistik, sehingga\n"
            "kesimpulan sebaiknya tidak digeneralisasi tanpa analisis lanjutan\n"
            "(misalnya dengan lag waktu, data intraday, atau model non-linear).\n"
        )

    print("Ringkasan hasil analisis disimpan ke:", OUTPUT_TXT)

    # 5. Membuat grafik dual-axis untuk salah satu koin sebagai ilustrasi
    df_grafik = src.utils.load_data(DATASET_PATH, koin=KOIN_UNTUK_GRAFIK)
    src.utils.buat_grafik_dual_axis(
        df_grafik,
        kolom_waktu="DateTime",
        kolom_harga="Price_USD",
        kolom_sentimen="Sentiment_Score",
        output_path=OUTPUT_PNG,
        judul=f"Harga vs Sentimen Pasar - {KOIN_UNTUK_GRAFIK}",
    )
    print("Grafik dual-axis disimpan ke:", OUTPUT_PNG)

    # 6. Membuat scatter plot untuk memvisualisasikan hubungan antara Sentiment_Score dan Volatility_Index
    src.utils.scatter_plot(
        df,
        kolom_x="Sentiment_Score",
        kolom_y="Volatility_Index",
        output_path="scatter_plot.png"
    )
    print("Scatter plot disimpan ke:", "scatter_plot.png")


if __name__ == "__main__":
    main()