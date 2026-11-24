"""
================================================================================
PRAKTIKUM 13 — PENGEMBANGAN WEB APP FUZZY DENGAN STREAMLIT
Pengujian Integrasi Komponen UI & Panduan Menjalankan Web App
--------------------------------------------------------------------------------
Nama : Hilmi Farel Arrazak (NIM: 240306013)
       Annisa Muzya Rafa
Modul: Modul 3 (Pertemuan 13)
Aplikasi: SmartRetail-Diskon (Sistem Penentuan Diskon Toko)
================================================================================
"""

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from fuzzy_engine import DiskonTokoFuzzyEngine


def verify_components():
    print("=" * 75)
    print("PRAKTIKUM 13: VERIFIKASI INTEGRASI MODUL & WEB APP STREAMLIT")
    print("=" * 75)

    # 1. Periksa berkas aplikasi
    app_path = os.path.join(CURRENT_DIR, "app.py")
    src_app_path = os.path.join(SRC_DIR, "app.py")
    modul3_app_path = os.path.join(PROJECT_ROOT, "Modul-3", "src", "app.py")

    print("1. PEMERIKSAAN BERKAS APLIKASI WEB:")
    print(f" - [ADA] Pertemuan13/app.py       : {os.path.exists(app_path)}")
    print(f" - [ADA] src/app.py               : {os.path.exists(src_app_path)}")
    print(f" - [ADA] Modul-3/src/app.py       : {os.path.exists(modul3_app_path)}")

    # 2. Pengujian Logika Engine
    print("\n2. PENGUJIAN LOGIKA INFERENSI ENGINE UNTUK TAMPILAN WEB:")
    engine = DiskonTokoFuzzyEngine()
    test_presets = [
        ("Pelanggan Baru (Belanja Rp 100rb, 2x/bln)", 100.0, 2.0),
        ("Pelanggan Reguler (Belanja Rp 500rb, 10x/bln)", 500.0, 10.0),
        ("Pelanggan VIP (Belanja Rp 900rb, 18x/bln)", 900.0, 18.0),
    ]

    for label, pem, frek in test_presets:
        res = engine.evaluate(pem, frek)
        print(f" Preset: {label}")
        print(f"   -> Diskon: {res['nilai_diskon']:.2f}% | Kategori: {res['kategori']} | Hemat: Rp {res['potongan_rp']:,.0f} | Bayar: Rp {res['total_bayar_rp']:,.0f}")

    print("\n" + "=" * 75)
    print("CARA MENJALANKAN APLIKASI WEB STREAMLIT:")
    print("=" * 75)
    print("Buka Terminal / Command Prompt pada folder proyek, lalu jalankan:")
    print("   streamlit run Modul-3/src/app.py")
    print("atau dari folder Pertemuan13:")
    print("   streamlit run app.py")
    print("\nAplikasi web interaktif akan otomatis terbuka pada browser di:")
    print("   http://localhost:8501")
    print("=" * 75)


if __name__ == "__main__":
    verify_components()
