===============================================================
UAS SAINS DATA (ST406)
APAKAH ‘HYPE’ PADA MEDIA SOCIAL BERKORELASI TERHADAP VOLATILITAS HARGA CRYPTO
===============================================================

Nama Mahasiswa   : Tarbiyah Wahidiyah
NIM              : 25.11.6568
Mata Kuliah      : Sains Data (ST406)


1. DESKRIPSI PROYEK
---------------------------------------------------------------
Proyek ini bertujuan untuk menganalisis hubungan antara sentimen
pasar (Sentiment_Score) dengan volatilitas harga (Volatility_Index)
pada beberapa aset cryptocurrency. Analisis dilakukan menggunakan
uji korelasi Pearson serta visualisasi deret waktu (time series)
untuk melihat pergerakan harga dibandingkan dengan sentimen pasar.


2. DATASET
---------------------------------------------------------------
File dataset   : dataset/data_mentah.csv
Sumber dataset : https://www.kaggle.com/datasets/shadab80k/crypto-market-sentiment-dataset-2026/data
Jumlah baris   : 3.650 baris
Rentang waktu  : 1 Januari 2024 s.d. 30 Desember 2025
Aset yang tercakup : Bitcoin, Ethereum, Solana, Cardano, Polkadot

Kolom pada dataset:
- Date                : tanggal pencatatan data
- Coin                : nama aset cryptocurrency
- Price_USD           : harga penutupan dalam USD
- Volume_24h          : volume transaksi dalam 24 jam terakhir
- Market_Cap          : kapitalisasi pasar
- Sentiment_Score     : skor sentimen pasar (rentang -1 sampai 1)
- Social_Mentions     : jumlah penyebutan di media sosial
- Volatility_Index    : indeks volatilitas harga

3. STRUKTUR FOLDER
---------------------------------------------------------------
proyek_akhir_ST406/
├── dataset/
│   └── data_mentah.csv     -> data mentah yang digunakan
├── hasil_txt/
│   └── hasil_analisis.txt  -> ringkasan hasil statistik (output)
├── src/
│   └──utils.py             -> kumpulan fungsi penunjang
├── VISUALISASI/
│   └──grafik_dual_axis.png -> visualisasi menggunakan grafik dual axis
│   └──scatter_plot.png     -> visualisasi menggunakan scatter plot
├── main.py                 -> file eksekusi utama
├── grafik_output.png       -> visualisasi harga vs sentimen (output)
└── README.txt              -> dokumentasi proyek (file ini)


4. METODE ANALISIS
---------------------------------------------------------------
- Pembersihan data: menghapus baris dengan nilai kosong pada
  kolom numerik utama, serta menyeragamkan format kolom waktu.
- Korelasi Pearson: mengukur kekuatan dan arah hubungan linear
  antara Sentiment_Score dan Volatility_Index, baik secara
  keseluruhan maupun per koin.
- Visualisasi dual-axis: menampilkan pergerakan Price_USD (sumbu
  kiri) dan Sentiment_Score (sumbu kanan) terhadap waktu untuk
  satu koin sebagai ilustrasi (default: Bitcoin, dapat diubah
  pada variabel KOIN_UNTUK_GRAFIK di main.py).


5. CARA MENJALANKAN
---------------------------------------------------------------
1) library:
   - pandas
   - scipy
   - matplotlib
   - seaborn
   - numpy

   Instalasi (jika belum ada):
   pip install pandas scipy matplotlib seabord numpy

2) Jalankan perintah berikut dari dalam folder proyek_akhir_ST406:
   python main.py

3) Program akan menghasilkan/memperbarui:
   - hasil_analisis.txt
   - grafik_dual_axis.png
   - scatter_plot.png


6. RINGKASAN TEMUAN AWAL
---------------------------------------------------------------
Berdasarkan hasil analisis pada dataset ini, korelasi antara
Sentiment_Score dan Volatility_Index secara keseluruhan maupun
per koin berada pada kisaran mendekati nol dan tidak signifikan
secara statistik (p >= 0.05). Hal ini mengindikasikan bahwa pada
data ini, sentimen pasar harian tidak menunjukkan hubungan linear
yang jelas dengan volatilitas harga. Detail lengkap dapat dilihat
pada file hasil_analisis.txt.
