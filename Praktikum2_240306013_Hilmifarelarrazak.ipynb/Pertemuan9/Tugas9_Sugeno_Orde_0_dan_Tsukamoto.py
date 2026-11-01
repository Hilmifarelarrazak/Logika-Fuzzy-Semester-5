
# ==========================================
# SISTEM PENENTUAN DISKON TOKO
# Perbandingan Sugeno Orde 0 dan Tsukamoto
# ==========================================

# 1. FUNGSI KEANGGOTAAN INPUT

def rendah(x):
    if x <= 25:
        return 1.0
    elif x >= 75:
        return 0.0
    return (75 - x) / 50


def tinggi(x):
    return 1 - rendah(x)


# 2. EMPAT ATURAN FUZZY
# R1: Pembelian sedikit AND Belanja jarang
# R2: Pembelian sedikit AND Belanja sering
# R3: Pembelian banyak AND Belanja jarang
# R4: Pembelian banyak AND Belanja sering


def hitung_alpha(pembelian, frekuensi):
    return [
        min(rendah(pembelian), rendah(frekuensi)),
        min(rendah(pembelian), tinggi(frekuensi)),
        min(tinggi(pembelian), rendah(frekuensi)),
        min(tinggi(pembelian), tinggi(frekuensi))
    ]


# ==========================================
# 3. METODE SUGENO ORDE 0
# ==========================================

def sugeno(alpha):
    nilai_konstanta = [10, 20, 30, 50]

    pembilang = sum(
        a * z for a, z in zip(alpha, nilai_konstanta)
    )

    penyebut = sum(alpha)

    if penyebut == 0:
        return 10

    return pembilang / penyebut


# ==========================================
# 4. METODE TSUKAMOTO
# ==========================================

def tsukamoto(alpha):

    # Fungsi konsekuen monoton untuk setiap aturan
    # R1: menurun, rentang 10-30%
    # R2: menaik, rentang 20-30%
    # R3: menaik, rentang 30-40%
    # R4: menaik, rentang 40-50%

    z1 = 30 - (20 * alpha[0])
    z2 = 20 + (10 * alpha[1])
    z3 = 30 + (10 * alpha[2])
    z4 = 40 + (10 * alpha[3])

    nilai_z = [z1, z2, z3, z4]

    pembilang = sum(
        a * z for a, z in zip(alpha, nilai_z)
    )

    penyebut = sum(alpha)

    if penyebut == 0:
        return 10

    return pembilang / penyebut


# ==========================================
# 5. PENGUJIAN 5 VARIASI INPUT
# ==========================================

data_uji = [
    (10, 15),
    (25, 35),
    (50, 50),
    (75, 70),
    (95, 90)
]

print("HASIL PERBANDINGAN SISTEM DISKON TOKO")
print("=" * 80)

print(
    f"{'Pembelian':<12}"
    f"{'Frekuensi':<12}"
    f"{'Sugeno':<18}"
    f"{'Tsukamoto':<18}"
    f"{'Selisih'}"
)

print("-" * 80)

for pembelian, frekuensi in data_uji:

    alpha = hitung_alpha(pembelian, frekuensi)

    hasil_sugeno = sugeno(alpha)
    hasil_tsukamoto = tsukamoto(alpha)

    selisih = abs(hasil_sugeno - hasil_tsukamoto)

    print(
        f"{pembelian:<12}"
        f"{frekuensi:<12}"
        f"{hasil_sugeno:<18.2f}"
        f"{hasil_tsukamoto:<18.2f}"
        f"{selisih:.2f}%"
    )

print("=" * 80)
print("Pengujian sistem selesai.")
