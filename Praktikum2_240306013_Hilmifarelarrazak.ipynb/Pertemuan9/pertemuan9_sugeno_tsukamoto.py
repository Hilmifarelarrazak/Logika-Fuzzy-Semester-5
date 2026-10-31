
import numpy as np

# =====================================================
# 1. INPUT SISTEM PENENTUAN DISKON TOKO
# =====================================================

lama_langganan = 15
frekuensi_transaksi = 8

# Derajat keanggotaan input sesuai sistem sebelumnya
mu_baru = 0.00
mu_lama = 0.75

mu_jarang = 0.20
mu_sering = 0.80

# =====================================================
# 2. FUZZY RULE BASE
# =====================================================

# R1: Baru AND Jarang -> Diskon Kecil
# R2: Baru AND Sering -> Diskon Sedang
# R3: Lama AND Jarang -> Diskon Sedang
# R4: Lama AND Sering -> Diskon Besar

alphas = [
    min(mu_baru, mu_jarang),
    min(mu_baru, mu_sering),
    min(mu_lama, mu_jarang),
    min(mu_lama, mu_sering)
]

print("NILAI FIRING STRENGTH")
for i, alpha in enumerate(alphas, 1):
    print(f"R{i}: {alpha:.2f}")

# =====================================================
# 3. FUNGSI PERHITUNGAN SUGENO
# =====================================================

def hitung_sugeno(alphas, z_values):
    total_alpha = np.sum(alphas)

    if total_alpha == 0:
        return 0.0

    return np.sum(np.array(alphas) * np.array(z_values)) / total_alpha


# =====================================================
# 4. SUGENO ORDE 0
# =====================================================

# Konstanta output setiap aturan (%)
z_sugeno0 = [5, 15, 15, 25]

hasil_sugeno0 = hitung_sugeno(alphas, z_sugeno0)


# =====================================================
# 5. SUGENO ORDE 1
# =====================================================

# Fungsi linear output berdasarkan input:
# z = a * lama_langganan
#   + b * frekuensi_transaksi + c

z_sugeno1 = [
    0.2 * lama_langganan + 0.3 * frekuensi_transaksi + 2,
    0.3 * lama_langganan + 0.4 * frekuensi_transaksi + 5,
    0.4 * lama_langganan + 0.2 * frekuensi_transaksi + 7,
    0.5 * lama_langganan + 0.5 * frekuensi_transaksi + 10
]

hasil_sugeno1 = hitung_sugeno(alphas, z_sugeno1)


# =====================================================
# 6. FUNGSI TSUKAMOTO
# =====================================================

# Fungsi output monoton:
# Diskon Kecil: menurun pada rentang 0-10
# Diskon Sedang: naik pada rentang 10-20
# Diskon Besar: naik pada rentang 20-30

def diskon_kecil(alpha):
    return 10 - (10 * alpha)

def diskon_sedang(alpha):
    return 10 + (10 * alpha)

def diskon_besar(alpha):
    return 20 + (10 * alpha)


# Nilai z untuk setiap aturan
z_tsukamoto = [
    diskon_kecil(alphas[0]),
    diskon_sedang(alphas[1]),
    diskon_sedang(alphas[2]),
    diskon_besar(alphas[3])
]

hasil_tsukamoto = hitung_sugeno(alphas, z_tsukamoto)


# =====================================================
# 7. MENAMPILKAN HASIL PERHITUNGAN
# =====================================================

print("\n" + "=" * 55)
print("SISTEM PENENTUAN DISKON TOKO")
print("KOMPARASI SUGENO DAN TSUKAMOTO")
print("=" * 55)

print("\nA. SUGENO ORDE 0")
print("Nilai output aturan:", z_sugeno0)
print(f"Hasil diskon: {hasil_sugeno0:.2f}%")

print("\nB. SUGENO ORDE 1")
print("Nilai output aturan:",
      [round(z, 2) for z in z_sugeno1])
print(f"Hasil diskon: {hasil_sugeno1:.2f}%")

print("\nC. TSUKAMOTO")
print("Nilai z setiap aturan:",
      [round(z, 2) for z in z_tsukamoto])
print(f"Hasil diskon: {hasil_tsukamoto:.2f}%")

print("\n" + "=" * 55)
print("TABEL PERBANDINGAN")
print("=" * 55)

print(f"{'Metode':<20} {'Diskon (%)':>15}")
print("-" * 37)

print(f"{'Sugeno Orde 0':<20} {hasil_sugeno0:>15.2f}")
print(f"{'Sugeno Orde 1':<20} {hasil_sugeno1:>15.2f}")
print(f"{'Tsukamoto':<20} {hasil_tsukamoto:>15.2f}")

print("=" * 55)
