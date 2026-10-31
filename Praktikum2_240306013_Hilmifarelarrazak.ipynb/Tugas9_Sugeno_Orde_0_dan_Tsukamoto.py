# ==========================================
# SISTEM PENGATURAN ALOKASI BANDWIDTH DINAMIS
# Perbandingan Sugeno Orde 0 dan Tsukamoto
# ==========================================

def rendah(x):
    if x <= 25:
        return 1.0
    elif x >= 75:
        return 0.0
    return (75 - x) / 50


def tinggi(x):
    return 1 - rendah(x)


# Empat aturan:
# R1: Pengguna sedikit AND Trafik rendah
# R2: Pengguna sedikit AND Trafik tinggi
# R3: Pengguna banyak AND Trafik rendah
# R4: Pengguna banyak AND Trafik tinggi

def hitung_alpha(pengguna, trafik):
    return [
        min(rendah(pengguna), rendah(trafik)),
        min(rendah(pengguna), tinggi(trafik)),
        min(tinggi(pengguna), rendah(trafik)),
        min(tinggi(pengguna), tinggi(trafik))
    ]


# ==========================================
# METODE SUGENO ORDE 0
# ==========================================

def sugeno(alpha):
    nilai_konstanta = [20, 40, 70, 100]

    pembilang = sum(a * z for a, z in zip(alpha, nilai_konstanta))
    penyebut = sum(alpha)

    if penyebut == 0:
        return 10

    return pembilang / penyebut


# ==========================================
# METODE TSUKAMOTO
# ==========================================

def tsukamoto(alpha):
    # Fungsi konsekuen monoton untuk setiap aturan
    # R1: menurun, rentang 10-30 Mbps
    # R2: menaik, rentang 30-50 Mbps
    # R3: menaik, rentang 50-80 Mbps
    # R4: menaik, rentang 80-100 Mbps

    z1 = 30 - (20 * alpha[0])
    z2 = 30 + (20 * alpha[1])
    z3 = 50 + (30 * alpha[2])
    z4 = 80 + (20 * alpha[3])

    nilai_z = [z1, z2, z3, z4]

    pembilang = sum(a * z for a, z in zip(alpha, nilai_z))
    penyebut = sum(alpha)

    if penyebut == 0:
        return 10

    return pembilang / penyebut


# ==========================================
# PENGUJIAN 5 VARIASI INPUT
# ==========================================

data_uji = [
    (10, 15),
    (25, 35),
    (50, 50),
    (75, 70),
    (95, 90)
]

print("HASIL PERBANDINGAN ALOKASI BANDWIDTH")
print("=" * 75)
print(f"{'Pengguna':<12}{'Trafik':<12}{'Sugeno':<18}{'Tsukamoto':<18}{'Selisih'}")
print("-" * 75)

for pengguna, trafik in data_uji:
    alpha = hitung_alpha(pengguna, trafik)

    hasil_sugeno = sugeno(alpha)
    hasil_tsukamoto = tsukamoto(alpha)

    selisih = abs(hasil_sugeno - hasil_tsukamoto)

    print(
        f"{pengguna:<12}{trafik:<12}"
        f"{hasil_sugeno:<18.2f}"
        f"{hasil_tsukamoto:<18.2f}"
        f"{selisih:.2f} Mbps"
    )