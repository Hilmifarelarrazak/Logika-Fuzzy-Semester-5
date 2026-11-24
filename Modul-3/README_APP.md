# 🛍️ PANDUAN PENGGUNA & DOKUMENTASI TEKNIS (USER GUIDE)
## SmartRetail-Diskon: Sistem Pendukung Keputusan Penentuan Diskon Toko Berbasis Logika Fuzzy Mamdani

**Pengembang:**
- **Hilmi Farel Arrazak** (NIM: 240306013)
- **Annisa Muzya Rafa**
- **Program Studi:** S1 Teknologi Informasi  
- **Mata Kuliah:** Praktikum Sistem Berbasis Pengetahuan / Kecerdasan Komputasional  
- **Modul:** Modul 3 (Pertemuan 11 - 14)

---

## 1. Deskripsi Singkat Aplikasi
**SmartRetail-Diskon** adalah sistem pendukung keputusan (*Decision Support System*) berbasis web yang memanfaatkan **Logika Fuzzy Mamdani** dengan metode defuzzifikasi **Centroid (Pusat Gravitasi)**. Sistem ini menggantikan aturan diskon konvensional yang kaku (*sharp boundary*) dengan pendekatan penilaian multi-derajat yang adil, proporsional, dan otomatis berdasarkan riwayat belanja serta loyalitas kunjungan pelanggan.

### Manfaat Utama:
1. **Personalisasi Promosi:** Menghilangkan diskon seragam (*flat discount*) yang memboroskan anggaran toko.
2. **Keadilan Konsumen:** Menghindari kekecewaan pembeli akibat ambang batas biner kaku (misal belanja Rp 499rb vs Rp 500rb).
3. **Optimasi Margin Profit Toko:** Memastikan diskon besar hanya diberikan kepada pelanggan yang terbukti loyal atau melakukan transaksi grosir dalam jumlah besar.

---

## 2. Prasyarat Instalasi (*Prerequisites*)
Aplikasi membutuhkan **Python 3.10+** serta pustaka dependensi yang tercantum pada file `requirements.txt`:

```bash
pip install -r requirements.txt
```

Isi berkas `requirements.txt`:
```text
streamlit>=1.30.0
numpy>=1.24.0
matplotlib>=3.7.0
pandas>=2.0.0
scikit-fuzzy>=0.4.2
```

---

## 3. Cara Menjalankan Aplikasi (*How to Run*)

### Metode A: Menggunakan Shortcut Batch (Paling Praktis di Windows)
Cukup klik dua kali berkas:
👉 **`jalankan_web_app.bat`** pada direktori utama proyek.

### Metode B: Menggunakan Terminal / PowerShell
Buka terminal di direktori proyek dan jalankan:
```powershell
python -m streamlit run "Modul3_240306013_Hilmifarelarrazak.ipynb\src\app.py"
```
Aplikasi web secara otomatis akan terbuka di peramban web pada alamat:
🌐 **`http://localhost:8501`**

---

## 4. Panduan Antarmuka Pengguna (*User Interface Guide*)

### 4.1 Panel Input (Sidebar)
1. **Mode Operasional:**
   - *Transaksi Kasir (Satuan):* Digunakan kasir saat melayani transaksi langsung di meja kasir.
   - *Evaluasi Massal (CSV):* Digunakan staf manajemen toko untuk menganalisis ratusan data transaksi sekaligus.
2. **Preset Profil Pelanggan (`st.selectbox`):**
   - Pilihan cepat untuk menguji profil belanja umum: *Pelanggan Baru*, *Pelanggan Reguler*, *Pelanggan VIP*, atau *Kustom*.
3. **Total Belanja Rupiah (`st.number_input`):**
   - Masukan nominal total belanja pelanggan (rentang valid: Rp 0 s.d. Rp 1.000.000).
4. **Frekuensi Kunjungan Bulanan (`st.slider`):**
   - Masukan jumlah kunjungan/transaksi belanja dalam satu bulan (rentang valid: 0 s.d. 20 kali/bulan).
5. **Validasi Batas Input & Error Handling (Praktikum 14):**
   - Terdapat panel validasi interaktif yang mendeteksi masukan tidak valid, angka negatif, atau nilai yang melebihi batas semesta secara seketika dan memberikan pesan error ramah pengguna (`st.sidebar.error`).

### 4.2 Panel Output Keputusan (Main Dashboard)
1. **Status Loyalty Badge:**
   - 🥉 **Bronze Member (Diskon Kecil):** Diskon dasar $< 20\%$ untuk apresiasi belanja standar.
   - 🥈 **Silver Member (Diskon Sedang):** Diskon loyalitas $20\% - 35\%$ untuk pelanggan rutin.
   - 🎉 **Gold / Platinum VIP (Diskon Besar):** Diskon apresiasi tertinggi $> 35\%$ untuk pembeli grosir/setia.
2. **Metric KPI Cards:**
   - *Besar Diskon (%):* Nilai numerik crisp hasil defuzzifikasi Centroid.
   - *Total Hemat (Rp):* Jumlah rupiah yang dipotong dari tagihan.
   - *Total Tagihan Bersih (Rp):* Jumlah rupiah final yang wajib dibayar pelanggan.
3. **Visualisasi Grafik Interaktif:**
   - *Kurva Aktivasi 9 Aturan (`Firing Rules Bar Chart`):* Menampilkan bobot derajat aktivasi $\alpha$ dari setiap aturan fuzzy.
   - *Kurva Agregasi & Defuzzifikasi Centroid:* Menampilkan daerah arsiran integrasi Mamdani dan letak garis defuzzifikasi.

---

## 5. Tabel Interpretasi Keputusan & Rekomendasi Kasir

| Kategori Diskon | Kisaran Diskon | Status Loyalty | Tindakan Operasional Kasir |
|:---:|:---:|:---:|:---|
| **Diskon Kecil** | $0.0\% - 19.9\%$ | **Bronze Member** | Berikan struk diskon reguler. Tawarkan program kartu member untuk meningkatkan kunjungan. |
| **Diskon Sedang** | $20.0\% - 34.9\%$ | **Silver Member** | Berikan apresiasi loyalitas. Tawarkan kupon promosi belanja berikutnya untuk retensi. |
| **Diskon Besar** | $35.0\% - 50.0\%$ | **Gold / VIP Member** | Berikan layanan prioritas kasir VIP dan ucapan terima kasih personal dari manajer toko. |

---

## 6. Tabel Laporan Pengujian Black-Box (Sesuai Format Bagian C)

Pengujian sistem dilakukan dengan metode **Boundary Value Analysis (BVA)** dan **Equivalence Partitioning** terhadap antarmuka dan mesin inferensi:

| ID Uji | Skenario Pengujian | Input 1 (Pembelian) | Input 2 (Frekuensi) | Output yang Diharapkan | Output Aktual Sistem | Status (Pass/Fail) |
|:---:|:---|:---:|:---:|:---|:---|:---:|
| **TC-01** | Batas Bawah Semesta | Rp 0 | 0.0 kali | Diskon Kecil ($< 15\%$) | Skor: 7.76% (Kecil) | **PASS** |
| **TC-02** | Batas Atas Semesta | Rp 1.000.000 | 20.0 kali | Diskon Besar ($> 40\%$) | Skor: 42.24% (Besar) | **PASS** |
| **TC-03** | Nilai Tengah (Transisi) | Rp 500.000 | 10.0 kali | Diskon Sedang ($20-30\%$) | Skor: 25.00% (Sedang) | **PASS** |
| **TC-04** | Belanja Sedikit, Frekuensi Maks | Rp 100.000 | 19.0 kali | Diskon Sedang (Apresiasi) | Skor: 25.00% (Sedang) | **PASS** |
| **TC-05** | Belanja Grosir Maks, Kunjungan Min | Rp 900.000 | 1.0 kali | Diskon Sedang | Skor: 25.00% (Sedang) | **PASS** |
| **TC-06** | Input Negatif (Di Luar Batas) | Rp -50.000 | 5.0 kali | Sistem Menolak / Pesan Error | Pesan Peringatan Ditampilkan (Validasi Berhasil) | **PASS** |
| **TC-07** | Input Melebihi Batas Semesta | Rp 1.500.000 | 25.0 kali | Sistem Menolak / Pesan Error | Pesan Peringatan Ditampilkan (Validasi Berhasil) | **PASS** |
| **TC-08** | Uji Kasus Tipikal A | Rp 150.000 | 2.0 kali | Diskon Kecil ($< 10\%$) | Skor: 7.76% (Kecil) | **PASS** |
| **TC-09** | Uji Kasus Tipikal B | Rp 450.000 | 8.0 kali | Diskon Sedang | Skor: 25.00% (Sedang) | **PASS** |
| **TC-10** | Uji Kasus Tipikal C | Rp 850.000 | 16.0 kali | Diskon Besar ($> 40\%$) | Skor: 42.24% (Besar) | **PASS** |

---
*Dokumentasi ini disusun untuk memenuhi tugas Asesmen Praktikum 14 Sistem Logika Fuzzy.*
