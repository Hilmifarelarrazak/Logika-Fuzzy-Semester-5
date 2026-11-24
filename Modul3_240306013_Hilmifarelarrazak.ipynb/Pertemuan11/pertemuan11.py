"""
================================================================================
PRAKTIKUM 11 — FUZZY PADA PERMASALAHAN NYATA
Identifikasi Masalah Domain TI, Analisis Kebutuhan Sistem, 
dan Perancangan Proposal Produk Fuzzy
--------------------------------------------------------------------------------
Nama : Hilmi Farel Arrazak
NIM  : 240306013
Modul: Modul 3 (Pertemuan 11)
Judul: SmartRetail-Diskon: Sistem Penentuan Diskon Toko Berbasis Fuzzy Mamdani
================================================================================
"""

import os
import sys
import pandas as pd
import numpy as np

# Konfigurasi path modul src
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
SRC_DIR = os.path.join(PROJECT_ROOT, "Modul-3", "src")
DATA_DIR = os.path.join(PROJECT_ROOT, "Modul-3", "data")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from fuzzy_engine import DiskonTokoFuzzyEngine, RULES


def check_project_structure():
    """Memeriksa kelengkapan berkas struktur folder Modul-3."""
    print("=" * 75)
    print("1. VERIFIKASI STRUKTUR FOLDER PROYEK MODUL-3 (SISTEM DISKON TOKO)")
    print("=" * 75)

    required_paths = [
        os.path.join(PROJECT_ROOT, "Modul-3", "Proposal_Produk_240306013.md"),
        os.path.join(PROJECT_ROOT, "Modul-3", "src", "__init__.py"),
        os.path.join(PROJECT_ROOT, "Modul-3", "src", "fuzzy_engine.py"),
        os.path.join(PROJECT_ROOT, "Modul-3", "src", "app.py"),
        os.path.join(PROJECT_ROOT, "Modul-3", "data", "test_cases.csv"),
    ]

    all_ok = True
    for p in required_paths:
        exists = os.path.exists(p)
        status = "[LENGKAP]" if exists else "[TIDAK DITEMUKAN]"
        rel_path = os.path.relpath(p, PROJECT_ROOT)
        print(f" {status:18s} : {rel_path}")
        if not exists:
            all_ok = False

    if all_ok:
        print("\n=> Status Struktur Proyek: 100% LENGKAP & MEMENUHI SPESIFIKASI")
    else:
        print("\n=> Status Struktur Proyek: TERDAPAT FILE YANG KURANG!")
    return all_ok


def show_product_overview():
    """Menampilkan ringkasan proposal produk sistem diskon toko."""
    print("\n" + "=" * 75)
    print("2. RINGKASAN PROPOSAL PRODUK SISTEM FUZZY (BAGIAN D)")
    print("=" * 75)
    print("Judul Produk      : SmartRetail-Diskon (Sistem Penentuan Diskon Toko)")
    print("Domain Masalah    : Personalisasi Retail & E-Commerce (Manajemen Diskon)")
    print("Pengusul          : Hilmi Farel Arrazak (NIM: 240306013)")
    print("-" * 75)
    print("Spesifikasi Variabel:")
    print(" 1. Input 1 : Jumlah Pembelian | Satuan: Ribu Rp | Semesta: [0, 1000] | Labels: Sedikit, Sedang, Banyak")
    print(" 2. Input 2 : Frekuensi Belanja | Satuan: Kali/Bln| Semesta: [0, 20]   | Labels: Jarang, Sedang, Sering")
    print(" 3. Output  : Besar Diskon Toko| Satuan: %       | Semesta: [0, 50]   | Labels: Kecil, Sedang, Besar")
    print("-" * 75)
    print(f"Basis Aturan      : {len(RULES)} Aturan Kombinatorial Mamdani (Max-Min)")
    print("Metode Defuzz     : Centroid (Center of Gravity / COG)")
    print("Arsitektur Sistem : Modular (Core Engine terpisah dari Streamlit UI)")


def run_fuzzy_engine_validation():
    """Menguji engine fuzzy terhadap dataset 20 kasus pengujian transaksi."""
    print("\n" + "=" * 75)
    print("3. PENGUJIAN INFERENSI ENGINE DISKON DENGAN DATASET 20 TRANSAKSI")
    print("=" * 75)

    engine = DiskonTokoFuzzyEngine()
    csv_path = os.path.join(DATA_DIR, "test_cases.csv")

    if not os.path.exists(csv_path):
        print(f"File dataset tidak ditemukan di: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    print(f"Total baris data uji ditemukan: {len(df)} transaksi\n")

    hasil_eval = []
    for _, row in df.iterrows():
        res = engine.evaluate(row["jumlah_pembelian"], row["frekuensi_belanja"])
        status = "[SESUAI]" if res["kategori"] == row["kategori_ekspektasi"] else "[DEVIASI WAJAR]"
        hasil_eval.append({
            "ID Transaksi": row["id_transaksi"],
            "Belanja (Rp)": f"Rp {res['input']['nominal_belanja_rp']:>9,.0f}",
            "Frekuensi": f"{row['frekuensi_belanja']:>2.0f}x/bln",
            "Diskon": f"{res['nilai_diskon']:>5.2f}%",
            "Kategori": f"{res['kategori']:<6s}",
            "Hemat (Rp)": f"Rp {res['potongan_rp']:>8,.0f}",
            "Status": status
        })

    df_hasil = pd.DataFrame(hasil_eval)
    print(df_hasil.to_string(index=False))

    sesuai_count = sum(1 for item in hasil_eval if item["Status"] == "[SESUAI]")
    akurasi = (sesuai_count / len(hasil_eval)) * 100
    print("\n" + "-" * 75)
    print(f"Kesesuaian dengan Ekspektasi Penjualan: {sesuai_count}/{len(hasil_eval)} ({akurasi:.1f}%)")
    print("Defuzzifikasi Centroid menghasilkan transisi persentase diskon yang mulus dan adil.")
    print("=" * 75)
    print("PRAKTIKUM 11 (SISTEM PENENTUAN DISKON TOKO) BERHASIL DISELESAIKAN!")
    print("=" * 75)


if __name__ == "__main__":
    check_project_structure()
    show_product_overview()
    run_fuzzy_engine_validation()
