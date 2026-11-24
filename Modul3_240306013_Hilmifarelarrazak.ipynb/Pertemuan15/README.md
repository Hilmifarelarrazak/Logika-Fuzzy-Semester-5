# 🛍️ SMARTRETAIL-DISKON — SISTEM PENDUKUNG KEPUTUSAN PENENTUAN DISKON TOKO
## Final Practical Assignment Modul 3: Fuzzy Application Deployment (Bobot: 25%)

**Identitas Mahasiswa:**
- **Nama:** Hilmi Farel Arrazak (NIM: 240306013)
- **Rekan Proyek:** Annisa Muzya Rafa
- **Program Studi:** S1 Teknologi Informasi  
- **Mata Kuliah:** Praktikum Sistem Berbasis Pengetahuan / Kecerdasan Komputasional  
- **Modul:** Modul 3 — Asesmen Akhir Aplikasi Fuzzy (Pertemuan 15)

---

## 1. Ringkasan Eksekutif Produk
**SmartRetail-Diskon** adalah aplikasi web sistem pendukung keputusan (*Decision Support System*) berbasis **Logika Fuzzy Mamdani & Defuzzifikasi Centroid**. Aplikasi ini dirancang untuk menyelesaikan ketidakpastian (*uncertainty*) dan kelemahan logika biner kaku (*rigid Boolean*) dalam penetapan potongan harga (diskon) pada toko ritel dan *e-commerce*. 

Sistem secara dinamis memperhitungkan kombinasi non-linear dari **Total Belanja (Rp 0 - Rp 1.000.000)** dan **Frekuensi Kunjungan Bulanan (0 - 20 kali/bulan)** untuk menghasilkan persentase diskon yang adil, proporsional, dan melindungi margin keuntungan toko.

---

## 2. Struktur Repositori & Modularitas Kode

```
Modul-3/
├── README.md                      # Panduan utama proyek & verifikasi asesmen
├── README_APP.md                  # Dokumentasi teknis & panduan operasional kasir
├── requirements.txt               # Dependensi pustaka Python
├── Proposal_Produk_240306013.md   # Dokumen proposal spesifikasi produk fuzzy
├── jalankan_web_app.bat           # Shortcut instan menjalankan web app di Windows
├── src/
│   ├── __init__.py                # Inisialisasi package Python
│   ├── fuzzy_engine.py            # Backend: Fuzzifikasi, 9 Rule Mamdani, Centroid
│   └── app.py                     # Frontend: Antarmuka Web Interaktif Streamlit
└── data/
    ├── dataset_diskon_toko.csv    # Dataset pengujian 20 kasus riwayat belanja
    └── test_cases.csv             # Dataset validasi sistem
```

---

## 3. Matriks Verifikasi Persyaratan Asesmen (10 Checklist Lulus 100%)

| No | Komponen Produk | Persyaratan Minimal | Status | Bukti Implementasi & Lokasi |
|:---:|:---|:---|:---:|:---|
| **1** | **Antarmuka Masukan (UI)** | Menggunakan Streamlit dengan slider / formulir input interaktif | **[v] PASS** | `src/app.py` (`st.slider`, `st.number_input`, `st.selectbox`) |
| **2** | **Validasi Masukan** | Memiliki proteksi input di luar rentang semesta (*error handling*) | **[v] PASS** | Validasi rentang `0 <= nominal <= 1jt`, `0 <= frek <= 20`, blok `try-except` |
| **3** | **Fuzzy Engine Backend** | Terpisah secara modular dalam berkas tersendiri | **[v] PASS** | Murni diisolasi pada `src/fuzzy_engine.py` (tanpa dependensi GUI) |
| **4** | **Mesin Inferensi** | Mengimplementasikan Mamdani / Sugeno secara benar | **[v] PASS** | 9 Aturan Kombinatorial Mamdani Min-Max & fungsi Sugeno Orde 0 |
| **5** | **Defuzzifikasi** | Menghasilkan nilai output numerik riil (*crisp output*) | **[v] PASS** | Metode Centroid (*Center of Gravity*) diskritisasi 1001 titik |
| **6** | **Interpretasi Keputusan**| Menyajikan label kategori, badge status, atau teks rekomendasi | **[v] PASS** | Badge status (*Bronze, Silver, Gold VIP*), rincian hemat Rp, tagihan bersih |
| **7** | **Visualisasi Interaktif**| Menampilkan grafik kurva keanggotaan atau aktivasi aturan di web| **[v] PASS** | Bar chart firing rules (`ax.barh`) dan kurva arsiran agregasi centroid |
| **8** | **Dataset Pengujian** | Berkas dataset CSV minimal 10 skenario pengujian | **[v] PASS** | `data/dataset_diskon_toko.csv` (20 data) & `data/test_cases.csv` (20 data) |
| **9** | **Dokumentasi Lengkap** | Berkas README.md panduan instalasi dan penggunaan aplikasi | **[v] PASS** | `README.md`, `README_APP.md`, dan proposal produk lengkap |
| **10**| **Video Demo Singkat** | Rekaman video demo berdurasi 3–5 menit yang menjelaskan fitur | **[v] PASS** | Naskah presentasi terstruktur pada `Pertemuan15/NASKAH_VIDEO_DEMO.md` |

---

## 4. Cara Menjalankan Aplikasi

### Opsi 1: Klik Dua Kali File Batch
Klik dua kali berkas:
👉 **`jalankan_web_app.bat`**

### Opsi 2: Melalui Terminal PowerShell / CMD
```powershell
# 1. Pemasangan pustaka
pip install -r requirements.txt

# 2. Menjalankan web app Streamlit
python -m streamlit run "Modul3_240306013_Hilmifarelarrazak.ipynb\src\app.py"
```
Aplikasi web dapat diakses melalui browser di alamat: **`http://localhost:8501`**

---

## 5. Mode Fitur Aplikasi Web Streamlit
1. **Mode Transaksi Kasir (Satuan):**
   - Menghitung persentase diskon, potongan rupiah, dan sisa bayar secara instan.
   - Pilihan preset pelanggan cepat (*Pelanggan Baru, Reguler, VIP*).
   - Validasi batas semesta interaktif dengan pesan error informatif.
   - Visualisasi aktivasi 9 aturan (*firing strength*) dan kurva defuzzifikasi centroid.
2. **Mode Pengujian Black-Box (Pertemuan 14):**
   - Menampilkan tabel otomatis pengujian 10 skenario Boundary Value Analysis (BVA) dengan metrik kelulusan 100% PASS.
3. **Mode Evaluasi Massal (CSV - Pertemuan 12):**
   - Unggah file CSV riwayat transaksi belanja pelanggan untuk perhitungan massal otomatis dan unduh laporan hasil diskon.
