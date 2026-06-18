# Last-Mile Delivery Optimization - UAS Praktikum Analisis Algoritma

<p align="center">
  <img src="data/diagram.png">
</p>

## Anggota Kelompok & Peran
- **Dean Frederic Wijaya (140810240027)**: Implementasi Algoritma (Eksak).
- **Hansel Stevan Boike (140810240079)**: Implementasi Algoritma(Heuristik) & Implementasi Data Loader.
- **Satrio Rafi Fahrezi (140810240063)**: Perancangan *Cost Function* & Beban Dinamis.
- **Steven Hapnico S.N. (140810240065)**: Pemodelan Skenario Ekonomi & Validasi Data.
- **Valensius Alven (140810240059)**: Analisis Keputusan Bisnis, Visualisasi Komparatif TCO, & Pelaporan Strategis.
- **Pemodelan Data**: Kolaborasi Tim (5 orang).

## Deskripsi Proyek
Proyek ini bertujuan untuk memecahkan dilema infrastruktur teknologi operasional pada perusahaan ekspedisi. Kami membandingkan dua pendekatan algoritma untuk menyelesaikan *Traveling Salesperson Problem* (TSP) dalam konteks pengantaran barang (*Last-Mile Delivery*):
1. **Algoritma Heuristik (Greedy Nearest Neighbor)**: Menawarkan kecepatan eksekusi instan namun dengan rute yang sub-optimal.
2. **Algoritma Eksak (Backtracking with Pruning)**: Menjamin rute terpendek absolut namun memerlukan biaya komputasi server yang lebih tinggi.

Analisis difokuskan pada **Total Cost of Ownership (TCO)** yang menggabungkan biaya bahan bakar (berdasarkan beban paket dinamis) dan biaya server komputasi awan.

## Panduan Menjalankan Program
Pastikan Anda memiliki Python 3 terinstal. Jalankan perintah berikut dari direktori utama proyek:

```bash
# Berpindah ke direktori source code
cd src

# Menjalankan laporan analisis keputusan bisnis
python report.py
```

## Hasil Simulasi & Komparasi

Berikut adalah visualisasi hasil eksekusi komparasi kedua algoritma pada skenario yang berbeda.

### Output Eksekusi Terminal
Menampilkan perincian komputasi jarak, waktu eksekusi, dan rincian biaya operasional:
![Screenshot Output Terminal](docs/terminal_output.png)

### Grafik Perbandingan TCO
Visualisasi perbandingan biaya total (TCO) antara algoritma Heuristik dan Eksak:
![Grafik Komparasi TCO](docs/tco_comparison.png)

## Analisis Algoritma

### 1. Heuristik (Greedy Nearest Neighbor)
- **Trade-off**: Fokus pada responsivitas sistem. Sangat efisien untuk jumlah titik pelanggan yang sangat besar di mana waktu eksekusi adalah prioritas.
- **Kompleksitas Waktu**: $O(N^2)$. Loop utama berjalan sebanyak $N$ kali untuk setiap titik, dan di dalamnya melakukan pencarian linear $O(N)$ untuk menemukan tetangga terdekat yang belum dikunjungi.
- **Kompleksitas Ruang**: $O(N)$ untuk menyimpan array status kunjungan dan urutan rute final.

### 2. Eksak (Backtracking with Pruning)
- **Trade-off**: Fokus pada efisiensi biaya bahan bakar. Menjamin penghematan jarak maksimal dengan memanfaatkan *Pruning* untuk memotong cabang rekursi yang tidak lebih baik dari solusi sementara.
- **Kompleksitas Waktu**: $O(N!)$. Eksplorasi permutasi rute secara mendalam. Meskipun *Pruning* mempercepat proses secara signifikan, kompleksitas teoritis tetap eksponensial.
- **Kompleksitas Ruang**: $O(N)$ untuk *recursion stack* dan penyimpanan jalur sementara.

## Analisis Keputusan Bisnis (Summary)
Berdasarkan hasil simulasi pada 13 lokasi pelanggan, kami menemukan korelasi kuat antara harga BBM dan efektivitas algoritma:

- **Skenario Subsidi (BBM Murah)**: Biaya server yang tinggi pada algoritma Eksak tidak sebanding dengan penghematan BBM yang dihasilkan. Dalam kondisi ini, **Heuristik** adalah pilihan yang paling menguntungkan.
- **Skenario Krisis (BBM Mahal)**: Penghematan jarak yang dihasilkan algoritma Eksak memberikan efisiensi biaya yang jauh lebih besar daripada tagihan server. Investasi pada algoritma yang lebih "pintar" memberikan ROI positif.
- **Titik Break-Even**: Algoritma Eksak mulai menunjukkan keunggulan finansial ketika harga BBM melampaui ambang batas tertentu di mana efisiensi operasional kendaraan menjadi lebih krusial daripada biaya komputasi.

**Kesimpulan**: Perusahaan disarankan untuk mengimplementasikan sistem *Switching* otomatis yang menggunakan Heuristik untuk operasional rutin dan beralih ke Eksak saat terjadi lonjakan harga energi atau untuk rute dengan beban paket yang sangat berat.
