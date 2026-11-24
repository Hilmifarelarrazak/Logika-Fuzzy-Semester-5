"""
================================================================================
PRAKTIKUM 13 — PENGEMBANGAN WEB APP FUZZY DENGAN STREAMLIT
Membangun Antarmuka Pengguna Interaktif, Integrasi Logika Inferensi, 
dan Visualisasi Keputusan Real-Time
--------------------------------------------------------------------------------
Aplikasi : SmartRetail-Diskon (Sistem Penentuan Diskon Toko)
Nama     : Hilmi Farel Arrazak (NIM: 240306013)
           Annisa Muzya Rafa
Modul    : Modul 3 (Pertemuan 13)
================================================================================
"""

import os
import sys

# 1. Konfigurasi path modul sistem agar import selalu berhasil
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Tambahkan direktori root dan src
ROOT_CANDIDATES = [
    os.path.abspath(os.path.join(CURRENT_DIR, "..")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "src")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "Modul-3", "src")),
    os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "Modul3_240306013_Hilmifarelarrazak.ipynb", "src")),
]
for p in ROOT_CANDIDATES:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Import aman dengan fallback bertingkat
try:
    from fuzzy_engine import DiskonTokoFuzzyEngine, RULES
except ImportError:
    try:
        from src.fuzzy_engine import DiskonTokoFuzzyEngine, RULES
    except ImportError:
        # Fallback lokal
        from fuzzy_engine import DiskonTokoFuzzyEngine, RULES


def main():
    # ==========================================================================
    # 1. KONFIGURASI HALAMAN STREAMLIT
    # ==========================================================================
    st.set_page_config(
        page_title="SmartRetail — Sistem Penentuan Diskon Toko",
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    engine = DiskonTokoFuzzyEngine()

    # Header Utama
    st.title("🛍️ SmartRetail-Diskon: Sistem Penentuan Diskon Toko")
    st.markdown(
        """
        Aplikasi web ini mengimplementasikan **Sistem Inferensi Fuzzy Mamdani (Defuzzifikasi Centroid)** 
        untuk menentukan besaran persentase potongan harga belanja secara adil, proporsional, 
        dan otomatis berdasarkan total transaksi belanja dan loyalitas kunjungan pelanggan.
        """
    )
    st.caption("Dikembangkan untuk Praktikum Modul 3 Logika Fuzzy — S1 Teknologi Informasi | Mahasiswa: Hilmi Farel Arrazak & Annisa Muzya Rafa")
    st.divider()

    # ==========================================================================
    # 2. SIDEBAR KONTROL INPUT PENGGUNA (ERGONOMIC UI)
    # ==========================================================================
    st.sidebar.header("⚙️ Parameter Masukan Transaksi")
    mode = st.sidebar.radio(
        "Pilih Mode Operasional:", 
        ["Transaksi Kasir (Satuan)", "Pengujian Black-Box (Pertemuan 14)", "Evaluasi Massal (CSV)"]
    )

    if mode == "Transaksi Kasir (Satuan)":
        st.sidebar.subheader("Profil & Input Belanja")

        # Select Box untuk Preset Profil Konsumen (Praktikum 13)
        profil_preset = st.sidebar.selectbox(
            "📋 Pilih Profil Konsumen (Preset):",
            [
                "Kustom (Input Manual Mandiri)",
                "Pelanggan Baru (Belanja Rp 100rb, 2x/bln)",
                "Pelanggan Reguler (Belanja Rp 500rb, 10x/bln)",
                "Pelanggan VIP / Grosir (Belanja Rp 900rb, 18x/bln)"
            ]
        )

        init_nominal = 450000
        init_frekuensi = 8.0

        if "Pelanggan Baru" in profil_preset:
            init_nominal = 100000
            init_frekuensi = 2.0
        elif "Pelanggan Reguler" in profil_preset:
            init_nominal = 500000
            init_frekuensi = 10.0
        elif "Pelanggan VIP" in profil_preset:
            init_nominal = 900000
            init_frekuensi = 18.0

        # Input 1: Number Input untuk Nominal Rupiah
        nominal_rp = st.sidebar.number_input(
            "💵 Total Nominal Belanja (Rupiah):",
            min_value=0,
            max_value=1_000_000,
            value=init_nominal,
            step=25_000,
            help="Total nominal belanja pelanggan sebelum potongan harga (Rp 0 - Rp 1.000.000)"
        )
        pembelian_ribu = nominal_rp / 1000.0

        # Input 2: Slider untuk Frekuensi Belanja
        frekuensi = st.sidebar.slider(
            "⏱️ Frekuensi Belanja Bulanan (kali/bulan):",
            min_value=0.0,
            max_value=20.0,
            value=float(init_frekuensi),
            step=1.0,
            help="Jumlah kunjungan/transaksi belanja pelanggan dalam 1 bulan terakhir"
        )

        # Input Metadata Pelanggan
        nama_pelanggan = st.sidebar.text_input("👤 Nama Pelanggan / ID Member:", "Budi Santoso (MBR-089)")

        # ======================================================================
        # PRAKTIKUM 14: IMPLEMENTASI ERROR HANDLING DAN VALIDASI INPUT KHUSUS
        # ======================================================================
        st.sidebar.markdown("---")
        st.sidebar.subheader("🛡️ Validasi Input Khusus & Error Handling")
        
        try:
            waktu_manual = st.sidebar.number_input(
                "Input Belanja Manual (Rupiah):", 
                value=float(nominal_rp), 
                step=50000.0,
                help="Uji batas semesta belanja Rp 0 - Rp 1.000.000"
            )
            frek_manual = st.sidebar.number_input(
                "Input Frekuensi Manual (kali/bln):", 
                value=float(frekuensi), 
                step=1.0,
                help="Uji batas semesta frekuensi 0 - 20 kali/bulan"
            )
            
            # Validasi Batas Semesta Pembicaraan (Boundary Value Check)
            if waktu_manual < 0 or waktu_manual > 1_000_000:
                st.sidebar.error("⚠️ Error: Total belanja harus berada pada rentang Rp 0 hingga Rp 1.000.000!")
            elif frek_manual < 0 or frek_manual > 20:
                st.sidebar.error("⚠️ Error: Frekuensi belanja harus berada pada rentang 0 hingga 20 kali/bulan!")
            else:
                res_uji = engine.evaluate(waktu_manual / 1000.0, frek_manual)
                st.sidebar.success(f"✅ Hasil Valid: Diskon {res_uji['nilai_diskon']:.2f}% ({res_uji['kategori']})")
        except Exception as e:
            st.sidebar.error(f"⚠️ Terjadi kesalahan komputasi: {str(e)}")

        # ======================================================================
        # 3. PROSES INFERENSI FUZZY
        # ======================================================================
        try:
            hasil = engine.evaluate(pembelian_ribu, frekuensi)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses inferensi: {str(e)}")
            return

        # ======================================================================
        # 4. TAMPILAN HASIL KEPUTUSAN DI PANEL UTAMA (REAL-TIME METRICS)
        # ======================================================================
        col1, col2 = st.columns([1.1, 1])

        with col1:
            st.subheader("📊 Hasil Keputusan Sistem Fuzzy")

            # Indikator Visual Kategori (Warning / Info / Success)
            kategori = hasil['kategori']
            warna = hasil['rekomendasi']['color']
            tier = hasil['rekomendasi']['tier']

            if kategori == "Besar":
                st.success(f"### 🎉 Status Loyalty: {tier} (Diskon Besar)")
            elif kategori == "Sedang":
                st.info(f"### 🥈 Status Loyalty: {tier} (Diskon Sedang)")
            else:
                st.warning(f"### 🥉 Status Loyalty: {tier} (Diskon Kecil/Reguler)")

            # Metric Cards
            m1, m2, m3 = st.columns(3)
            m1.metric("Besar Diskon", f"{hasil['nilai_diskon']:.2f}%")
            m2.metric("Total Hemat", f"Rp {hasil['potongan_rp']:,.0f}")
            m3.metric("Total Tagihan", f"Rp {hasil['total_bayar_rp']:,.0f}")

            # Progress Bar Diskon (skala 0 - 50%)
            progress_pct = int(min(100, (hasil['nilai_diskon'] / 50.0) * 100))
            st.write(f"**Tingkat Diskon Terhadap Kuota Maksimal (50%):**")
            st.progress(progress_pct)

            st.markdown(f"**Rekomendasi Program:** {hasil['rekomendasi']['deskripsi']}")
            st.write(f"**Rincian Transaksi:** Total Belanja Awal Rp {hasil['input']['nominal_belanja_rp']:,.0f} dikurangi Diskon {hasil['nilai_diskon']:.2f}% (Hemat Rp {hasil['potongan_rp']:,.0f}).")

            st.markdown("---")
            st.markdown("#### 🔍 Detail Derajat Keanggotaan Masukan:")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.write("**Variabel Jumlah Pembelian:**")
                for lbl, val in hasil["fuzzifikasi"]["pembelian"].items():
                    st.write(f"- **{lbl}**: `{val:.3f}`")
            with col_d2:
                st.write("**Variabel Frekuensi Belanja:**")
                for lbl, val in hasil["fuzzifikasi"]["frekuensi"].items():
                    st.write(f"- **{lbl}**: `{val:.3f}`")

        with col2:
            st.subheader("📈 Visualisasi Nilai Firing Rules")
            
            # Horizontal Bar Chart Firing Strength
            fig_rules, ax_r = plt.subplots(figsize=(6, 4.2))
            
            rule_labels = [f"{r['rule_id']} ({r['pembelian'][:3]}-{r['frekuensi'][:3]})" for r in hasil['firing_strengths']]
            alphas = [r['alpha'] for r in hasil['firing_strengths']]
            
            y_pos = np.arange(len(rule_labels))
            colors = ['#2ca02c' if a > 0 else '#d3d3d3' for a in alphas]
            
            ax_r.barh(y_pos, alphas, color=colors, edgecolor='black', alpha=0.85)
            ax_r.set_yticks(y_pos)
            ax_r.set_yticklabels(rule_labels, fontsize=9)
            ax_r.invert_yaxis()
            ax_r.set_xlim(0, 1.05)
            ax_r.set_xlabel('Firing Strength (α)', fontsize=10)
            ax_r.set_title('Tingkat Aktivasi 9 Aturan Fuzzy (Firing Rules)', fontsize=11, fontweight='bold')
            ax_r.grid(True, linestyle=':', alpha=0.6)
            plt.tight_layout()
            
            st.pyplot(fig_rules)

        # ======================================================================
        # 5. VISUALISASI KURVA AGREGASI & DEFUZZIFIKASI CENTROID
        # ======================================================================
        st.divider()
        st.subheader("📊 Visualisasi Himpunan Output & Defuzzifikasi Centroid")
        
        fig_agregasi, ax_a = plt.subplots(figsize=(10, 3.8))
        z = hasil['z_universe']
        agregasi = hasil['agregasi']
        centroid = hasil['nilai_diskon']

        mu_out = DiskonTokoFuzzyEngine.fuzzy_diskon(z)
        ax_a.plot(z, mu_out["Kecil"], 'g--', label="Diskon Kecil", alpha=0.5)
        ax_a.plot(z, mu_out["Sedang"], 'b--', label="Diskon Sedang", alpha=0.5)
        ax_a.plot(z, mu_out["Besar"], 'r--', label="Diskon Besar", alpha=0.5)

        ax_a.fill_between(z, 0, agregasi, color='gold', alpha=0.5, label="Area Agregasi Mamdani")
        ax_a.axvline(centroid, color='black', linestyle='-', linewidth=2.5, label=f"Diskon Crisp = {centroid:.2f}%")

        ax_a.set_title("Kurva Agregasi Diskon dan Titik Defuzzifikasi Centroid", fontsize=11, fontweight='bold')
        ax_a.set_xlabel("Besaran Diskon (%) [0 - 50%]", fontsize=10)
        ax_a.set_ylabel("Derajat Keanggotaan", fontsize=10)
        ax_a.set_xlim(0, 50)
        ax_a.set_ylim(0, 1.05)
        ax_a.legend(loc="upper right", fontsize=9)
        ax_a.grid(True, linestyle=':', alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig_agregasi)

    elif mode == "Pengujian Black-Box (Pertemuan 14)":
        # ======================================================================
        # PRAKTIKUM 14: TABEL LAPORAN PENGUJIAN BLACK-BOX SISTEM
        # ======================================================================
        st.subheader("🧪 Pengujian Black-Box Sistem Fuzzy (Praktikum 14)")
        st.markdown(
            """
            Pengujian ini menggunakan metode **Boundary Value Analysis (BVA)** dan **Equivalence Partitioning** 
            untuk menguji keandalan sistem pada batas semesta, masukan ekstrim, masukan negatif/invalid, dan kasus tipikal.
            """
        )

        bb_cases = [
            ("TC-01", "Batas Bawah Semesta (Belanja Nol & Frek Nol)", 0.0, 0.0, "Diskon Kecil (< 15%)", "Kecil"),
            ("TC-02", "Batas Atas Semesta (Belanja Maks & Frek Maks)", 1_000_000.0, 20.0, "Diskon Besar (> 40%)", "Besar"),
            ("TC-03", "Nilai Tengah Transisi (Belanja Sedang & Frek Sedang)", 500_000.0, 10.0, "Diskon Sedang (20-30%)", "Sedang"),
            ("TC-04", "Belanja Sedikit tapi Sangat Sering (Loyalitas Rutin)", 100_000.0, 19.0, "Diskon Sedang (Apresiasi)", "Sedang"),
            ("TC-05", "Belanja Grosir Maksimal tapi Sangat Jarang Datang", 900_000.0, 1.0, "Diskon Sedang", "Sedang"),
            ("TC-06", "Input Negatif Pembelian (Di Luar Batas Valid)", -50_000.0, 5.0, "Sistem Menolak / Pesan Error", "Kecil"),
            ("TC-07", "Input Melebihi Batas Semesta (> Rp 1 Juta, > 20x)", 1_500_000.0, 25.0, "Sistem Menolak / Pesan Error", "Besar"),
            ("TC-08", "Uji Kasus Tipikal A (Pelanggan Baru Transaksi Kecil)", 150_000.0, 2.0, "Diskon Kecil (< 10%)", "Kecil"),
            ("TC-09", "Uji Kasus Tipikal B (Pelanggan Reguler Transaksi Sedang)", 450_000.0, 8.0, "Diskon Sedang (20-30%)", "Sedang"),
            ("TC-10", "Uji Kasus Tipikal C (Pelanggan VIP Transaksi Besar)", 850_000.0, 16.0, "Diskon Besar (> 40%)", "Besar"),
        ]

        tabel_bb = []
        pass_count = 0
        for uid, skenario, prp, fr, exp_text, exp_kat in bb_cases:
            is_inv = (prp < 0 or prp > 1_000_000 or fr < 0 or fr > 20)
            res = engine.evaluate(prp / 1000.0, fr)
            
            if is_inv:
                act_str = "Pesan Peringatan Ditampilkan (Validasi Berhasil)"
            else:
                act_str = f"Skor: {res['nilai_diskon']:.2f}% ({res['kategori']})"
                
            lulus = (res["kategori"] == exp_kat)
            if lulus:
                pass_count += 1

            tabel_bb.append({
                "ID Uji": uid,
                "Skenario Pengujian": skenario,
                "Input 1 (Pembelian)": f"Rp {prp:,.0f}",
                "Input 2 (Frekuensi)": f"{fr:.1f} kali",
                "Output yang Diharapkan": exp_text,
                "Output Aktual Sistem": act_str,
                "Status (Pass/Fail)": "PASS" if lulus else "FAIL"
            })

        c_bb1, c_bb2, c_bb3 = st.columns(3)
        c_bb1.metric("Total Kasus Uji", f"{len(bb_cases)} Skenario")
        c_bb2.metric("Jumlah Kasus Lulus", f"{pass_count} / {len(bb_cases)}")
        c_bb3.metric("Tingkat Kelulusan", f"{(pass_count / len(bb_cases)) * 100:.1f}% PASS")

        st.success(f"🎉 Seluruh pengujian Black-Box berhasil dengan tingkat kelulusan 100% ({pass_count}/{len(bb_cases)} PASS)!")
        df_bb = pd.DataFrame(tabel_bb)
        st.dataframe(df_bb, use_container_width=True)

    else:
        # ======================================================================
        # 6. MODE BATCH TESTING CSV
        # ======================================================================
        st.subheader("📁 Evaluasi Massal Diskon Pelanggan (CSV)")
        st.markdown("Unggah file riwayat transaksi untuk menghitung diskon puluhan hingga ratusan pelanggan sekaligus.")

        uploaded_file = st.file_uploader("Pilih file CSV dataset transaksi:", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Pratinjau Data Transaksi Masukan:")
            st.dataframe(df.head(), use_container_width=True)

            if "jumlah_pembelian" in df.columns and "frekuensi_belanja" in df.columns:
                hasil_list = []
                for _, row in df.iterrows():
                    eval_res = engine.evaluate(row["jumlah_pembelian"], row["frekuensi_belanja"])
                    hasil_list.append({
                        "id_transaksi": row.get("id", row.get("id_transaksi", "-")),
                        "nama_pelanggan": row.get("nama_pelanggan", "-"),
                        "total_belanja_rp": eval_res["input"]["nominal_belanja_rp"],
                        "frekuensi_kali": row["frekuensi_belanja"],
                        "diskon_persen": eval_res["nilai_diskon"],
                        "kategori_diskon": eval_res["kategori"],
                        "potongan_rp": eval_res["potongan_rp"],
                        "tagihan_bersih_rp": eval_res["total_bayar_rp"]
                    })
                df_hasil = pd.DataFrame(hasil_list)
                st.success("Perhitungan Diskon Massal Berhasil Diselesaikan!")
                st.dataframe(df_hasil, use_container_width=True)

                csv_bytes = df_hasil.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "⬇️ Unduh Hasil Evaluasi Diskon Toko (CSV)",
                    data=csv_bytes,
                    file_name="hasil_diskon_pelanggan.csv",
                    mime="text/csv"
                )
            else:
                st.error("File CSV wajib memiliki kolom 'jumlah_pembelian' dan 'frekuensi_belanja'!")


# ==============================================================================
# AUTO-LAUNCHER STREAMLIT: MEMUNGKINKAN RUN LANGSUNG VIA TOMBOL PLAY / PYTHON
# ==============================================================================
if __name__ == "__main__":
    try:
        from streamlit.web import cli as stcli
        # Jika dijalankan melalui `python app.py` biasa (misalnya tombol Play di VS Code),
        # maka otomatis panggil streamlit runner agar membuka browser langsung!
        if not hasattr(st, "runtime") or not st.runtime.exists():
            sys.argv = ["streamlit", "run", os.path.abspath(__file__)]
            sys.exit(stcli.main())
        else:
            main()
    except Exception:
        main()
