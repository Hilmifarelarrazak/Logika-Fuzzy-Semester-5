
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz


# ==========================================================
# 1. DEFINISI SEMESTA DAN FUNGSI KEANGGOTAAN DISKON
# ==========================================================

z = np.linspace(0, 30, 1000)

mf_diskon_kecil = fuzz.trimf(z, [0, 5, 12])
mf_diskon_sedang = fuzz.trimf(z, [8, 15, 22])
mf_diskon_besar = fuzz.trimf(z, [18, 25, 30])


# ==========================================================
# 2. NILAI KEANGGOTAAN INPUT
# ==========================================================

lama = {
    "Baru": 0.0,
    "Lama": 0.75
}

frekuensi = {
    "Jarang": 0.20,
    "Sering": 0.80
}


# ==========================================================
# 3. BASIS ATURAN FUZZY (4 RULE)
# ==========================================================

rules = [
    ("Baru", "Jarang", "Kecil"),
    ("Baru", "Sering", "Sedang"),
    ("Lama", "Jarang", "Sedang"),
    ("Lama", "Sering", "Besar")
]


# ==========================================================
# 4. EVALUASI SELURUH ATURAN FUZZY
# ==========================================================

print("=" * 60)
print("SISTEM PENENTUAN DISKON TOKO DENGAN METODE MAMDANI")
print("=" * 60)

hasil_alpha = {}

for i, (l, f, d) in enumerate(rules, start=1):

    alpha = min(lama[l], frekuensi[f])
    hasil_alpha[i] = alpha

    print(f"\nRULE {i}")
    print(f"IF Lama Langganan {l}")
    print(f"AND Frekuensi Transaksi {f}")
    print(f"THEN Diskon {d}")
    print(f"Firing Strength (alpha) = {alpha:.2f}")

    if alpha > 0:
        print("Status: AKTIF")
    else:
        print("Status: TIDAK AKTIF")

print("\nJumlah aturan aktif:",
      sum(a > 0 for a in hasil_alpha.values()),
      "dari 4 aturan")


# ==========================================================
# 5. IMPLIKASI MAMDANI (MIN)
# ==========================================================

imp_kecil = np.fmin(
    hasil_alpha[1], mf_diskon_kecil
)

imp_sedang_1 = np.fmin(
    hasil_alpha[2], mf_diskon_sedang
)

imp_sedang_2 = np.fmin(
    hasil_alpha[3], mf_diskon_sedang
)

imp_besar = np.fmin(
    hasil_alpha[4], mf_diskon_besar
)


# ==========================================================
# 6. AGREGASI (MAX)
# ==========================================================

agregasi_sedang = np.fmax(
    imp_sedang_1, imp_sedang_2
)

agregasi = np.fmax(
    imp_kecil,
    np.fmax(agregasi_sedang, imp_besar)
)


# ==========================================================
# 7. PERHITUNGAN 5 METODE DEFUZZIFIKASI
# ==========================================================

defuzz_methods = [
    "centroid",
    "bisector",
    "mom",
    "som",
    "lom"
]

hasil_defuzz = {}

for method in defuzz_methods:

    nilai = fuzz.defuzz(z, agregasi, method)
    hasil_defuzz[method] = nilai


# ==========================================================
# 8. MENAMPILKAN HASIL DEFUZZIFIKASI
# ==========================================================

print("\n")
print("=" * 60)
print("HASIL KOMPARASI 5 METODE DEFUZZIFIKASI")
print("=" * 60)

for method, nilai in hasil_defuzz.items():

    print(f"Metode {method.upper():<12}: {nilai:.3f}%")

print("=" * 60)


# ==========================================================
# 9. SATU GRAFIK PERBANDINGAN 5 METODE DEFUZZIFIKASI
# ==========================================================

plt.figure(figsize=(12, 6.5))

# Kurva agregasi fuzzy
plt.plot(
    z,
    agregasi,
    color="blue",
    linewidth=2.5,
    label="Kurva Agregasi Fuzzy"
)

plt.fill_between(
    z,
    0,
    agregasi,
    color="skyblue",
    alpha=0.4
)

# Warna setiap metode
colors = {
    "centroid": "red",
    "bisector": "purple",
    "mom": "black",
    "som": "green",
    "lom": "orange"
}

# Garis hasil defuzzifikasi
for method, nilai in hasil_defuzz.items():

    plt.axvline(
        x=nilai,
        color=colors[method],
        linestyle="--",
        linewidth=2,
        label=f"{method.upper()} ({nilai:.2f}%)"
    )

    idx = np.abs(z - nilai).argmin()

    plt.scatter(
        [nilai],
        [agregasi[idx]],
        color=colors[method],
        s=60,
        zorder=6
    )

plt.title(
    "Perbandingan 5 Metode Defuzzifikasi Mamdani",
    fontsize=13,
    fontweight="bold"
)

plt.xlabel("Besaran Diskon (%)", fontsize=11)
plt.ylabel("Derajat Keanggotaan μ(z)", fontsize=11)

plt.ylim(-0.05, 1.05)

plt.grid(True, linestyle=":", alpha=0.6)

plt.legend(loc="upper right", fontsize=9)

plt.tight_layout()

plt.savefig(
    "komparasi_metode_defuzzifikasi_diskon.png",
    dpi=300
)

plt.show()
