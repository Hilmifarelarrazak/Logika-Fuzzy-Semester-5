"""
================================================================================
MODUL LOGIKA INFERENSI FUZZY MAMDANI & SUGENO (CORE ENGINE)
Sistem Pendukung Keputusan Penentuan Diskon Toko Retail & E-Commerce
Nama : Hilmi Farel Arrazak (NIM: 240306013)
     : Annisa Muzya Rafa
================================================================================
"""

from typing import Dict, Tuple, List, Any
import numpy as np


# ==============================================================================
# 1. FUNGSI KEANGGOTAAN DASAR
# ==============================================================================

def trapezoid(x: np.ndarray, a: float, b: float, c: float, d: float) -> np.ndarray:
    """Fungsi keanggotaan kurva trapesium."""
    x = np.asarray(x, dtype=float)
    if a == b:
        left = np.where(x >= b, 1.0, 0.0)
    else:
        left = np.clip((x - a) / (b - a), 0.0, 1.0)
        
    if c == d:
        right = np.where(x <= c, 1.0, 0.0)
    else:
        right = np.clip((d - x) / (d - c), 0.0, 1.0)
        
    return np.minimum(left, right)


def triangle(x: np.ndarray, a: float, b: float, c: float) -> np.ndarray:
    """Fungsi keanggotaan kurva segitiga."""
    x = np.asarray(x, dtype=float)
    if b == a:
        left = np.where(x >= b, 1.0, 0.0)
    else:
        left = (x - a) / (b - a)
        
    if c == b:
        right = np.where(x <= b, 1.0, 0.0)
    else:
        right = (c - x) / (c - b)
        
    return np.maximum(0.0, np.minimum(left, right))


# ==============================================================================
# 2. BASIS ATURAN (9 RULES MAMDANI DISKON TOKO)
# ==============================================================================

RULES: List[Tuple[str, str, str]] = [
    # Pembelian, Frekuensi Belanja, Besar Diskon
    ("Sedikit", "Jarang", "Kecil"),   # R1
    ("Sedikit", "Sedang", "Kecil"),   # R2
    ("Sedikit", "Sering", "Sedang"),  # R3
    ("Sedang",  "Jarang", "Kecil"),   # R4
    ("Sedang",  "Sedang", "Sedang"),  # R5
    ("Sedang",  "Sering", "Besar"),   # R6
    ("Banyak",  "Jarang", "Sedang"),  # R7
    ("Banyak",  "Sedang", "Besar"),   # R8
    ("Banyak",  "Sering", "Besar"),   # R9
]


# ==============================================================================
# 3. KELAS UTAMA ENGINE FUZZY DISKON TOKO (MAMDANI)
# ==============================================================================

class DiskonTokoFuzzyEngine:
    """
    Mesin inferensi fuzzy Mamdani untuk penentuan besaran diskon toko ritel.
    """

    # Domain Semesta Pembicaraan
    PEMBELIAN_MIN, PEMBELIAN_MAX = 0.0, 1000.0   # Ribu Rupiah (0 - 1.000.000 Rp)
    FREKUENSI_MIN, FREKUENSI_MAX = 0.0, 20.0     # Kali transaksi per bulan
    DISKON_MIN, DISKON_MAX       = 0.0, 50.0     # Persentase diskon (0 - 50%)

    def __init__(self, resolusi: int = 1001):
        self.resolusi = resolusi
        self.z_universe = np.linspace(self.DISKON_MIN, self.DISKON_MAX, self.resolusi)

    @staticmethod
    def fuzzy_pembelian(x: float) -> Dict[str, float]:
        """Menghitung derajat keanggotaan variabel Jumlah Pembelian."""
        x = float(np.clip(x, DiskonTokoFuzzyEngine.PEMBELIAN_MIN, DiskonTokoFuzzyEngine.PEMBELIAN_MAX))
        return {
            "Sedikit": float(trapezoid(x, 0.0, 0.0, 150.0, 350.0)),
            "Sedang":  float(triangle(x, 250.0, 500.0, 750.0)),
            "Banyak":  float(trapezoid(x, 650.0, 850.0, 1000.0, 1000.0))
        }

    @staticmethod
    def fuzzy_frekuensi(y: float) -> Dict[str, float]:
        """Menghitung derajat keanggotaan variabel Frekuensi Belanja."""
        y = float(np.clip(y, DiskonTokoFuzzyEngine.FREKUENSI_MIN, DiskonTokoFuzzyEngine.FREKUENSI_MAX))
        return {
            "Jarang": float(trapezoid(y, 0.0, 0.0, 3.0, 7.0)),
            "Sedang": float(triangle(y, 5.0, 10.0, 15.0)),
            "Sering": float(trapezoid(y, 12.0, 16.0, 20.0, 20.0))
        }

    @classmethod
    def fuzzy_diskon(cls, z: np.ndarray) -> Dict[str, np.ndarray]:
        """Menghitung kurva keanggotaan variabel Output Besar Diskon."""
        return {
            "Kecil":  trapezoid(z, 0.0, 0.0, 10.0, 20.0),
            "Sedang": triangle(z, 15.0, 25.0, 35.0),
            "Besar":  trapezoid(z, 30.0, 40.0, 50.0, 50.0)
        }

    def evaluate(self, pembelian: float, frekuensi: float) -> Dict[str, Any]:
        """
        Menjalankan proses inferensi Mamdani & Defuzzifikasi Centroid:
        Input:
            pembelian : Total transaksi dalam Ribu Rupiah (contoh: 450 = Rp 450.000)
            frekuensi : Frekuensi transaksi belanja per bulan (contoh: 8 kali)
        Output:
            dict ringkasan hasil evaluasi diskon
        """
        pembelian_clamped = float(np.clip(pembelian, self.PEMBELIAN_MIN, self.PEMBELIAN_MAX))
        frekuensi_clamped = float(np.clip(frekuensi, self.FREKUENSI_MIN, self.FREKUENSI_MAX))

        # 1. Fuzzifikasi
        mu_pembelian = self.fuzzy_pembelian(pembelian_clamped)
        mu_frekuensi = self.fuzzy_frekuensi(frekuensi_clamped)

        # 2. Kurva output diskon
        mu_output = self.fuzzy_diskon(self.z_universe)

        # Inisialisasi agregasi
        hasil_agregasi = np.zeros_like(self.z_universe)
        firing_strengths = []

        # 3. Evaluasi 9 Aturan
        for idx, (lbl_pem, lbl_frek, lbl_out) in enumerate(RULES, start=1):
            alpha = min(mu_pembelian[lbl_pem], mu_frekuensi[lbl_frek])
            firing_strengths.append({
                "rule_id": f"R{idx}",
                "pembelian": lbl_pem,
                "frekuensi": lbl_frek,
                "diskon": lbl_out,
                "alpha": float(alpha)
            })

            # Implikasi MIN
            hasil_rule = np.minimum(alpha, mu_output[lbl_out])
            # Agregasi MAX
            hasil_agregasi = np.maximum(hasil_agregasi, hasil_rule)

        # 4. Defuzzifikasi Centroid
        area_sum = np.sum(hasil_agregasi)
        if area_sum == 0:
            nilai_diskon = 0.0
        else:
            nilai_diskon = float(np.sum(self.z_universe * hasil_agregasi) / area_sum)

        # 5. Klasifikasi Kategori Diskon
        keanggotaan_diskon = {
            "Kecil":  float(trapezoid(nilai_diskon, 0.0, 0.0, 10.0, 20.0)),
            "Sedang": float(triangle(nilai_diskon, 15.0, 25.0, 35.0)),
            "Besar":  float(trapezoid(nilai_diskon, 30.0, 40.0, 50.0, 50.0))
        }

        kategori_terpilih = max(keanggotaan_diskon, key=keanggotaan_diskon.get)

        rekomendasi_kupon = {
            "Kecil": {
                "badge": "DISKON REGULER",
                "tier": "Bronze Member",
                "deskripsi": "Apresiasi belanja reguler toko (Diskon dasar < 20%).",
                "color": "#6c757d"
            },
            "Sedang": {
                "badge": "DISKON LOYALTI",
                "tier": "Silver Member",
                "deskripsi": "Insentif belanja moderat untuk meningkatkan retensi (20% - 35%).",
                "color": "#0d6efd"
            },
            "Besar": {
                "badge": "DISKON VIP SPESIAL",
                "tier": "Gold / Platinum Member",
                "deskripsi": "Apresiasi pembeli prioritas tertinggi / belanja borongan (> 35%).",
                "color": "#198754"
            }
        }

        nominal_belanja_rp = pembelian * 1000.0
        potongan_rp = (nilai_diskon / 100.0) * nominal_belanja_rp
        total_bayar_rp = nominal_belanja_rp - potongan_rp

        return {
            "input": {
                "jumlah_pembelian_ribu": pembelian,
                "nominal_belanja_rp": nominal_belanja_rp,
                "frekuensi_belanja": frekuensi
            },
            "fuzzifikasi": {
                "pembelian": mu_pembelian,
                "frekuensi": mu_frekuensi
            },
            "firing_strengths": firing_strengths,
            "nilai_diskon": round(nilai_diskon, 2),
            "kategori": kategori_terpilih,
            "potongan_rp": round(potongan_rp, 0),
            "total_bayar_rp": round(total_bayar_rp, 0),
            "rekomendasi": rekomendasi_kupon[kategori_terpilih],
            "z_universe": self.z_universe,
            "agregasi": hasil_agregasi
        }


# ==============================================================================
# 4. FUNGSI INFERENSI SUGENO TAMBAHAN (SESUAI DOKUMEN MODUL 13)
# ==============================================================================

def hitung_prioritas_tiket(waktu_jam: float, urgensi_skor: float):
    """
    Fungsi logika inferensi fuzzy Sugeno Orde 0 untuk tiket TI
    (disediakan untuk kompatibilitas pengujian modul praktikum 13).
    """
    mu_waktu_cepat = max(0.0, min(1.0, (8.0 - waktu_jam) / 8.0)) if waktu_jam <= 8.0 else 0.0
    mu_waktu_lama = max(0.0, min(1.0, (waktu_jam - 4.0) / 12.0)) if waktu_jam >= 4.0 else 0.0
    
    mu_urgensi_rendah = max(0.0, min(1.0, (50.0 - urgensi_skor) / 50.0)) if urgensi_skor <= 50.0 else 0.0
    mu_urgensi_tinggi = max(0.0, min(1.0, (urgensi_skor - 30.0) / 70.0)) if urgensi_skor >= 30.0 else 0.0
    
    a1 = min(mu_waktu_cepat, mu_urgensi_rendah)
    z1 = 20.0
    a2 = min(mu_waktu_cepat, mu_urgensi_tinggi)
    z2 = 60.0
    a3 = min(mu_waktu_lama, mu_urgensi_rendah)
    z3 = 50.0
    a4 = min(mu_waktu_lama, mu_urgensi_tinggi)
    z4 = 95.0
    
    total_alpha = a1 + a2 + a3 + a4
    if total_alpha == 0:
        skor = 20.0
    else:
        skor = (a1*z1 + a2*z2 + a3*z3 + a4*z4) / total_alpha
        
    skor = round(float(skor), 2)
    
    if skor < 35.0:
        kategori = "Rendah"
    elif skor < 65.0:
        kategori = "Sedang"
    elif skor < 85.0:
        kategori = "Tinggi"
    else:
        kategori = "Kritis (Eskalasi Segera)"
        
    return skor, kategori, {
        "alpha": [a1, a2, a3, a4],
        "mu_input": {
            "Waktu Cepat": mu_waktu_cepat, "Waktu Lama": mu_waktu_lama,
            "Urgensi Rendah": mu_urgensi_rendah, "Urgensi Tinggi": mu_urgensi_tinggi
        }
    }


# ==============================================================================
# PENGUJIAN MANDIRI
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("SMARTRETAIL DISKON TOKO ENGINE TEST (MAMDANI CENTROID)")
    print("=" * 70)

    engine = DiskonTokoFuzzyEngine()
    test_cases = [
        (100.0, 2.0),
        (250.0, 10.0),
        (500.0, 10.0),
        (750.0, 15.0),
        (900.0, 18.0),
    ]

    for i, (pem, frek) in enumerate(test_cases, 1):
        res = engine.evaluate(pem, frek)
        print(f"Kasus {i:02d}: Belanja=Rp {res['input']['nominal_belanja_rp']:,.0f} | "
              f"Frekuensi={frek:2.0f}x/bln => Diskon={res['nilai_diskon']:5.2f}% ({res['kategori']:6s}) | "
              f"Hemat=Rp {res['potongan_rp']:,.0f} | Bayar=Rp {res['total_bayar_rp']:,.0f}")
