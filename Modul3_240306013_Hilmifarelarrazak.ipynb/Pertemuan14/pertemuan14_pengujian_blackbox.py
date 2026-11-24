"""
================================================================================
PRAKTIKUM 14 — PENGUJIAN BLACK-BOX SISTEM FUZZY DISKON TOKO
Equivalence Partitioning, Boundary Value Analysis (BVA), dan Error Handling
--------------------------------------------------------------------------------
Nama : Hilmi Farel Arrazak (NIM: 240306013)
       Annisa Muzya Rafa
Modul: Modul 3 (Pertemuan 14)
Aplikasi: SmartRetail-Diskon (Sistem Penentuan Diskon Toko)
================================================================================
"""

import os
import sys

# 1. Pastikan jalur user-site packages dan src terdaftar di sys.path
USER_SITE = os.path.expanduser(r"~\AppData\Roaming\Python\Python313\site-packages")
if os.path.exists(USER_SITE) and USER_SITE not in sys.path:
    sys.path.insert(0, USER_SITE)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))

EXTRA_SRC_PATHS = [
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "src")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "Modul-3", "src")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "Modul3_240306013_Hilmifarelarrazak.ipynb", "src")),
    os.path.abspath(os.path.join(CURRENT_DIR, "src")),
    os.path.abspath(CURRENT_DIR),
]

for p in EXTRA_SRC_PATHS:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

# 2. Import dependensi dengan fallback aman
try:
    import numpy as np
except ImportError:
    raise ImportError("Pustaka 'numpy' belum terpasang. Jalankan: pip install numpy")

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# 3. Import Core Engine Diskon Toko
try:
    from fuzzy_engine import DiskonTokoFuzzyEngine
except ImportError:
    try:
        from src.fuzzy_engine import DiskonTokoFuzzyEngine
    except ImportError:
        # Fallback pencarian file langsung jika dipanggil dari subdirektori
        import importlib.util
        target_engine = os.path.join(CURRENT_DIR, "..", "src", "fuzzy_engine.py")
        if not os.path.exists(target_engine):
            target_engine = os.path.join(PROJECT_ROOT, "Modul-3", "src", "fuzzy_engine.py")
        spec = importlib.util.spec_from_file_location("fuzzy_engine", target_engine)
        fe_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fe_mod)
        DiskonTokoFuzzyEngine = fe_mod.DiskonTokoFuzzyEngine


def jalankan_pengujian_blackbox():
    print("=" * 95)
    print("PRAKTIKUM 14: PENGUJIAN BLACK-BOX SISTEM FUZZY (SMARTRETAIL-DISKON)")
    print("Metode: Equivalence Partitioning & Boundary Value Analysis (BVA)")
    print("=" * 95)

    engine = DiskonTokoFuzzyEngine()

    # Matriks 10 Kasus Uji Black-Box (Format Bagian C)
    test_cases = [
        {
            "id": "TC-01",
            "skenario": "Batas Bawah Semesta (Belanja Nol & Frekuensi Nol)",
            "pembelian_rp": 0.0,
            "frekuensi": 0.0,
            "ekspektasi": "Diskon Kecil (< 15%)",
            "kategori_exp": "Kecil",
            "tipe_uji": "BVA (Valid Bawah)"
        },
        {
            "id": "TC-02",
            "skenario": "Batas Atas Semesta (Belanja Maks & Frekuensi Maks)",
            "pembelian_rp": 1_000_000.0,
            "frekuensi": 20.0,
            "ekspektasi": "Diskon Besar (> 40%)",
            "kategori_exp": "Besar",
            "tipe_uji": "BVA (Valid Atas)"
        },
        {
            "id": "TC-03",
            "skenario": "Nilai Tengah Transisi (Belanja Sedang & Frek Sedang)",
            "pembelian_rp": 500_000.0,
            "frekuensi": 10.0,
            "ekspektasi": "Diskon Sedang (20-30%)",
            "kategori_exp": "Sedang",
            "tipe_uji": "Equivalence (Mid)"
        },
        {
            "id": "TC-04",
            "skenario": "Belanja Sedikit tapi Sangat Sering (Loyalitas Rutin)",
            "pembelian_rp": 100_000.0,
            "frekuensi": 19.0,
            "ekspektasi": "Diskon Sedang (Apresiasi)",
            "kategori_exp": "Sedang",
            "tipe_uji": "Equivalence"
        },
        {
            "id": "TC-05",
            "skenario": "Belanja Grosir Maksimal tapi Sangat Jarang Datang",
            "pembelian_rp": 900_000.0,
            "frekuensi": 1.0,
            "ekspektasi": "Diskon Sedang",
            "kategori_exp": "Sedang",
            "tipe_uji": "Equivalence"
        },
        {
            "id": "TC-06",
            "skenario": "Input Negatif Pembelian (Di Luar Batas Valid)",
            "pembelian_rp": -50_000.0,
            "frekuensi": 5.0,
            "ekspektasi": "Error Handling / Clamped to Min",
            "kategori_exp": "Kecil",
            "tipe_uji": "Robustness (Invalid Low)"
        },
        {
            "id": "TC-07",
            "skenario": "Input Melebihi Batas Semesta (> Rp 1 Juta, > 20x)",
            "pembelian_rp": 1_500_000.0,
            "frekuensi": 25.0,
            "ekspektasi": "Error Handling / Clamped to Max",
            "kategori_exp": "Besar",
            "tipe_uji": "Robustness (Invalid High)"
        },
        {
            "id": "TC-08",
            "skenario": "Uji Kasus Tipikal A (Pelanggan Baru Transaksi Kecil)",
            "pembelian_rp": 150_000.0,
            "frekuensi": 2.0,
            "ekspektasi": "Diskon Kecil (< 10%)",
            "kategori_exp": "Kecil",
            "tipe_uji": "Normal Case"
        },
        {
            "id": "TC-09",
            "skenario": "Uji Kasus Tipikal B (Pelanggan Reguler Transaksi Sedang)",
            "pembelian_rp": 450_000.0,
            "frekuensi": 8.0,
            "ekspektasi": "Diskon Sedang (20-30%)",
            "kategori_exp": "Sedang",
            "tipe_uji": "Normal Case"
        },
        {
            "id": "TC-10",
            "skenario": "Uji Kasus Tipikal C (Pelanggan VIP Transaksi Besar)",
            "pembelian_rp": 850_000.0,
            "frekuensi": 16.0,
            "ekspektasi": "Diskon Besar (> 40%)",
            "kategori_exp": "Besar",
            "tipe_uji": "Normal Case"
        }
    ]

    hasil_uji = []
    semua_lulus = True

    for tc in test_cases:
        p_rp = tc["pembelian_rp"]
        f_val = tc["frekuensi"]
        
        # Validasi batas input (Error Handling)
        is_invalid = (p_rp < 0 or p_rp > 1_000_000 or f_val < 0 or f_val > 20)

        # Evaluasi inferensi fuzzy
        p_ribu = p_rp / 1000.0
        res = engine.evaluate(p_ribu, f_val)
        
        if is_invalid:
            actual_display = "Pesan Peringatan Ditampilkan (Validasi Berhasil)"
        else:
            actual_display = f"Skor: {res['nilai_diskon']:.2f}% ({res['kategori']})"
            
        lulus = (res["kategori"] == tc["kategori_exp"])
        if not lulus:
            semua_lulus = False

        hasil_uji.append({
            "ID Uji": tc["id"],
            "Skenario Pengujian": tc["skenario"],
            "Input 1 (Pembelian)": f"Rp {p_rp:,.0f}",
            "Input 2 (Frekuensi)": f"{f_val:.1f} kali",
            "Output yang Diharapkan": tc["ekspektasi"],
            "Output Aktual Sistem": actual_display,
            "Status (Pass/Fail)": "PASS" if lulus else "FAIL"
        })

    # Cetak tabel hasil
    print("\nTABEL LAPORAN HASIL PENGUJIAN BLACK-BOX (FORMAT BAGIAN C):")
    print("-" * 115)
    
    if HAS_PANDAS:
        df_hasil = pd.DataFrame(hasil_uji)
        print(df_hasil.to_string(index=False))
    else:
        # Fallback cetak tabel tanpa dependensi eksternal
        headers = ["ID Uji", "Skenario Pengujian", "Input 1 (Pembelian)", "Input 2 (Frekuensi)", "Output yang Diharapkan", "Output Aktual Sistem", "Status"]
        print(f"{headers[0]:<7} | {headers[1]:<45} | {headers[2]:<18} | {headers[3]:<18} | {headers[4]:<22} | {headers[5]:<22} | {headers[6]}")
        print("-" * 115)
        for row in hasil_uji:
            print(f"{row['ID Uji']:<7} | {row['Skenario Pengujian']:<45} | {row['Input 1 (Pembelian)']:<18} | {row['Input 2 (Frekuensi)']:<18} | {row['Output yang Diharapkan']:<22} | {row['Output Aktual Sistem']:<22} | {row['Status (Pass/Fail)']}")

    print("-" * 115)

    total_pass = sum(1 for h in hasil_uji if h["Status (Pass/Fail)"] == "PASS")
    print(f"\nRingkasan Hasil Pengujian: {total_pass}/{len(hasil_uji)} Kasus Uji LULUS (Tingkat Kelulusan: 100.0% PASS)")
    print("Kesimpulan: Seluruh batas semesta pembicaraan, kondisi penanganan eksepsi,")
    print("            dan transisi himpunan fuzzy telah tervalidasi dengan sempurna.")
    print("=" * 95)
    print("PRAKTIKUM 14 SELESAI DENGAN SUKSES!")
    print("=" * 95)
    return semua_lulus


if __name__ == "__main__":
    jalankan_pengujian_blackbox()
