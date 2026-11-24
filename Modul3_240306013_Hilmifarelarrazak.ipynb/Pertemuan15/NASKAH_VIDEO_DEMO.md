# 🎬 NASKAH DAN PANDUAN PEREKAMAN VIDEO DEMONSTRASI PRODUK (3–5 MENIT)
## Asesmen Akhir Modul 3: SmartRetail-Diskon

**Identitas Mahasiswa:**
- **Nama:** Hilmi Farel Arrazak (NIM: 240306013)
- **Rekan:** Annisa Muzya Rafa
- **Mata Kuliah:** Praktikum Sistem Berbasis Pengetahuan
- **Judul Aplikasi:** SmartRetail-Diskon (Sistem Penentuan Diskon Toko Berbasis Logika Fuzzy Mamdani)
- **Durasi Video:** 3 – 5 Menit

---

### Rencana Alur Waktu (*Timeline Video Demo*)

```
[00:00 - 00:45] Pembukaan & Latar Belakang Masalah
      ▼
[00:45 - 01:45] Arsitektur Sistem & Logika Fuzzy Mamdani
      ▼
[01:45 - 03:00] Demonstrasi Langsung Aplikasi Web Streamlit (Single Transaction)
      ▼
[03:00 - 03:45] Uji Validasi Masukan, Error Handling & Black-Box Testing
      ▼
[03:45 - 04:30] Demonstrasi Batch Testing CSV & Penutup
```

---

### Bagian 1: Pembukaan & Latar Belakang Masalah (Durasi: 00:00 - 00:45)
*Tampilan Layar: Halaman Utama Aplikasi Web Streamlit atau Slide Judul Proyek.*

> **Skrip Presenter:**
> *"Halo, selamat pagi/siang kepada Bapak/Ibu dosen pengampu dan rekan-rekan sekalian. Perkenalkan saya **Hilmi Farel Arrazak** dengan NIM **240306013**, bersama rekan saya **Annisa Muzya Rafa**. 
> Pada kesempatan asesmen akhir Modul 3 ini, kami mempersembahkan produk aplikasi pendukung keputusan bernama **SmartRetail-Diskon**.
> Masalah nyata yang kami angkat adalah dilema penetapan diskon pada toko ritel. Selama ini, diskon seragam atau aturan Boolean kaku sering kali tidak adil bagi pembeli setia dan merugikan margin toko. Oleh karena itu, kami membangun sistem berbasis **Logika Fuzzy Mamdani** untuk mengotomatisasi persentase diskon belanja secara adil, mulus, dan proporsional."*

---

### Bagian 2: Arsitektur Sistem & Penjelasan Engine Fuzzy (Durasi: 00:45 - 01:45)
*Tampilan Layar: Menunjukkan struktur folder `src/fuzzy_engine.py` dan diagram alur DFD.*

> **Skrip Presenter:**
> *"Aplikasi kami dibangun dengan arsitektur bersih yang memisahkan logika komputasi inti di berkas `fuzzy_engine.py` dengan antarmuka web di `app.py`.
> Sistem menggunakan 2 variabel input:
> 1. **Jumlah Pembelian** dari Rp 0 hingga Rp 1.000.000, dengan himpunan Sedikit, Sedang, dan Banyak.
> 2. **Frekuensi Belanja** dari 0 hingga 20 kali per bulan, dengan himpunan Jarang, Sedang, dan Sering.
> 
> Seluruh input dievaluasi melalui **9 aturan kombinatorial Mamdani** menggunakan operator MIN, lalu digabungkan dengan agregasi MAX, dan dikonversi menjadi persentase diskon riil 0 hingga 50 persen menggunakan metode defuzzifikasi **Centroid (Pusat Gravitasi)**."*

---

### Bagian 3: Demonstrasi Fitur Utama Antarmuka Streamlit (Durasi: 01:45 - 03:00)
*Tampilan Layar: Buka browser `http://localhost:8501`, ubah nilai slider dan tunjukkan metrik.*

> **Skrip Presenter:**
> *"Sekarang mari kita uji coba aplikasi webnya secara langsung:
> 1. Pertama, kami sediakan fitur **Preset Profil Konsumen**. Jika kita pilih 'Pelanggan Baru', sistem otomatis mengatur belanja Rp 100.000 dengan kunjungan 2 kali per bulan. Terlihat di panel utama, pelanggan mendapatkan diskon dasar 7.76% dengan status **Bronze Member**.
> 2. Jika kita geser slider ke nominal belanja Rp 500.000 dan frekuensi 10 kali/bulan, diskon otomatis naik secara mulus ke angka 25.00% dengan status **Silver Member**. Pelanggan hemat Rp 125.000 dari total tagihan.
> 3. Dan untuk pembeli VIP grosir dengan belanja Rp 900.000 dan frekuensi 18 kali/bulan, sistem langsung memberikan apresiasi maksimal sebesar 42.24% dengan status **Gold/Platinum VIP**.
> 4. Di bagian grafik sebelah kanan, terlihat visualisasi **Firing Strength** yang menunjukkan aturan mana saja yang aktif secara real-time, serta grafik kurva area agregasi Mamdani lengkap dengan garis tegak titik berat defuzzifikasi Centroid-nya."*

---

### Bagian 4: Pengujian Validasi & Error Handling (Durasi: 03:00 - 03:45)
*Tampilan Layar: Klik panel 'Validasi Input Khusus & Error Handling' di sidebar, masukkan angka negatif.*

> **Skrip Presenter:**
> *"Sesuai kriteria Asesmen Modul 3 dan pengujian Black-Box di Pertemuan 14, sistem kami lengkapi dengan penanganan kesalahan (*error handling*).
> Apabila pengguna secara tidak sengaja memasukkan angka negatif, misalnya belanja Rp -50.000, sistem secara proaktif memunculkan pesan error berwarna merah yang ramah pengguna: *'⚠️ Error: Total belanja harus berada pada rentang Rp 0 hingga Rp 1.000.000!'*. Sistem tetap aman dari crash (*robust*) dan tidak mengalami instabilitas numerik.
> Kami juga telah menguji 10 kasus uji Boundary Value Analysis pada tab 'Pengujian Black-Box' dengan tingkat kelulusan 100% PASS."*

---

### Bagian 5: Demonstrasi Batch Testing CSV & Penutup (Durasi: 03:45 - 04:30)
*Tampilan Layar: Pindah ke mode 'Evaluasi Massal (CSV)', unggah `dataset_diskon_toko.csv`, klik unduh hasil.*

> **Skrip Presenter:**
> *"Terakhir, untuk kebutuhan manajerial toko, kami menyediakan mode **Evaluasi Massal CSV**. Kita cukup mengunggah berkas `dataset_diskon_toko.csv` yang berisi 20 transaksi riil, dan sistem dalam sekejap menghitung seluruh diskon pelanggan secara serentak. Hasilnya pun dapat langsung diunduh kembali dalam format CSV.
> 
> Demikian presentasi dan demonstrasi aplikasi **SmartRetail-Diskon**. Produk ini telah memenuhi seluruh 10 checklist kriteria Asesmen Akhir Modul 3. Terima kasih atas perhatian Bapak/Ibu dosen pengampu. Wassalamu'alaikum warahmatullahi wabarakatuh."*
