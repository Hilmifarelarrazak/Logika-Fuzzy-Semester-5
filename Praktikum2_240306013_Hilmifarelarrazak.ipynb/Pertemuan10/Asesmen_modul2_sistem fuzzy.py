
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D


# ==================================================
# 1. FUNGSI KEANGGOTAAN FUZZY
# ==================================================

def trapezoid(x, a, b, c, d):
    x = np.asarray(x, dtype=float)

    # Sisi kiri
    if a == b:
        left = np.ones_like(x) if np.ndim(x) > 0 else 1.0
        left = np.where(x >= b, left, 0.0)
    else:
        left = np.clip((x - a) / (b - a), 0, 1)

    # Sisi kanan
    if c == d:
        right = np.where(x <= c, 1.0, 0.0)
    else:
        right = np.clip((d - x) / (d - c), 0, 1)

    return np.minimum(left, right)


def triangle(x, a, b, c):
    x = np.asarray(x, dtype=float)

    left = (x - a) / (b - a)
    right = (c - x) / (c - b)

    return np.maximum(0, np.minimum(left, right))


# ==================================================
# 2. VARIABEL INPUT WAKTU RESPONS
# Universe: 0-10 jam
# ==================================================

def fuzzy_waktu(x):
    return {
        "Cepat": trapezoid(x, 0, 0, 2, 4),
        "Sedang": triangle(x, 2, 5, 8),
        "Lambat": trapezoid(x, 6, 8, 10, 10)
    }


# ==================================================
# 3. VARIABEL INPUT TINGKAT DAMPAK
# Universe: 0-100 persen
# ==================================================

def fuzzy_dampak(x):
    return {
        "Rendah": trapezoid(x, 0, 0, 20, 40),
        "Sedang": triangle(x, 30, 50, 70),
        "Tinggi": trapezoid(x, 60, 80, 100, 100)
    }


# ==================================================
# 4. VARIABEL OUTPUT TINGKAT URGENSI
# Universe: 0-100
# ==================================================

def fuzzy_output(x):
    return {
        "Rendah": trapezoid(x, 0, 0, 20, 40),
        "Sedang": triangle(x, 30, 50, 70),
        "Tinggi": trapezoid(x, 60, 80, 100, 100)
    }


# ==================================================
# 5. BASIS ATURAN FUZZY (9 RULE)
# ==================================================

aturan = [
    ("Cepat", "Rendah", "Rendah"),
    ("Cepat", "Sedang", "Rendah"),
    ("Cepat", "Tinggi", "Sedang"),

    ("Sedang", "Rendah", "Rendah"),
    ("Sedang", "Sedang", "Sedang"),
    ("Sedang", "Tinggi", "Tinggi"),

    ("Lambat", "Rendah", "Sedang"),
    ("Lambat", "Sedang", "Tinggi"),
    ("Lambat", "Tinggi", "Tinggi")
]


# ==================================================
# 6. PROSES INFERENSI MAMDANI
# DAN DEFUZZIFIKASI CENTROID
# ==================================================

def evaluasi_sistem_fuzzy(waktu, dampak):

    mu_waktu = fuzzy_waktu(waktu)
    mu_dampak = fuzzy_dampak(dampak)

    z = np.linspace(0, 100, 1001)

    mu_output = fuzzy_output(z)

    hasil_agregasi = np.zeros_like(z)

    nilai_alpha = []

    # Evaluasi setiap aturan
    for input_waktu, input_dampak, output in aturan:

        # Operator AND menggunakan MIN
        alpha = min(
            mu_waktu[input_waktu],
            mu_dampak[input_dampak]
        )

        nilai_alpha.append(alpha)

        # Implikasi Mamdani menggunakan MIN
        hasil_rule = np.minimum(
            alpha,
            mu_output[output]
        )

        # Agregasi menggunakan MAX
        hasil_agregasi = np.maximum(
            hasil_agregasi,
            hasil_rule
        )

    # Defuzzifikasi menggunakan Centroid
    if np.sum(hasil_agregasi) == 0:
        nilai_urgensi = 0
    else:
        nilai_urgensi = (
            np.sum(z * hasil_agregasi) /
            np.sum(hasil_agregasi)
        )

    # Menentukan kategori hasil
    keanggotaan_hasil = fuzzy_output(nilai_urgensi)

    kategori = max(
        keanggotaan_hasil,
        key=keanggotaan_hasil.get
    )

    return nilai_urgensi, kategori, z, hasil_agregasi


# ==================================================
# 7. PENGUJIAN 5 SKENARIO
# ==================================================

print("=" * 55)
print("SISTEM PENENTUAN TINGKAT URGENSI TIKET HELPDESK TI")
print("METODE FUZZY MAMDANI")
print("=" * 55)

data_uji = [
    (1, 10),
    (3, 35),
    (5, 50),
    (7, 75),
    (9, 95)
]

print("\nHASIL PENGUJIAN 5 SKENARIO")
print("-" * 55)

for i, (waktu, dampak) in enumerate(data_uji, start=1):

    hasil, kategori, z, agregasi = evaluasi_sistem_fuzzy(
        waktu, dampak
    )

    print(f"\nPengujian {i}")
    print(f"Waktu Respons  : {waktu} jam")
    print(f"Tingkat Dampak : {dampak}%")
    print(f"Nilai Urgensi  : {hasil:.2f}")
    print(f"Kategori       : {kategori}")


# ==================================================
# 8. INPUT DATA DARI PENGGUNA
# ==================================================

print("\n" + "=" * 55)
print("MASUKKAN DATA TIKET HELPDESK")
print("=" * 55)

try:
    waktu = float(input("Masukkan Waktu Respons (0-10 jam): "))
    dampak = float(input("Masukkan Tingkat Dampak (0-100%): "))

    if not (0 <= waktu <= 10):
        raise ValueError("Waktu respons harus antara 0 sampai 10.")

    if not (0 <= dampak <= 100):
        raise ValueError("Tingkat dampak harus antara 0 sampai 100.")

    hasil, kategori, z, agregasi = evaluasi_sistem_fuzzy(
        waktu, dampak
    )

    print("\nHASIL PENENTUAN URGENSI TIKET")
    print("-" * 55)
    print(f"Waktu Respons  : {waktu} jam")
    print(f"Tingkat Dampak : {dampak}%")
    print(f"Nilai Urgensi  : {hasil:.2f}")
    print(f"Kategori       : {kategori}")

except ValueError as error:
    print("\nInput tidak valid:", error)
    raise SystemExit


# ==================================================
# 9. GRAFIK AGREGASI FUZZY
# ==================================================

plt.figure(figsize=(10, 5))

plt.plot(z, agregasi, label="Hasil Agregasi Fuzzy")

plt.axvline(
    hasil,
    linestyle="--",
    label=f"Centroid = {hasil:.2f}"
)

plt.title("Grafik Agregasi Fuzzy Mamdani")
plt.xlabel("Tingkat Urgensi")
plt.ylabel("Derajat Keanggotaan")
plt.xlim(0, 100)
plt.ylim(0, 1.1)
plt.grid(True)
plt.legend()

plt.savefig("grafik_agregasi.png")
plt.show()


# ==================================================
# 10. GRAFIK DECISION SURFACE 3D
# ==================================================

waktu_range = np.linspace(0, 10, 30)
dampak_range = np.linspace(0, 100, 30)

X, Y = np.meshgrid(waktu_range, dampak_range)

Z = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):

        nilai, kategori, _, _ = evaluasi_sistem_fuzzy(
            X[i, j],
            Y[i, j]
        )

        Z[i, j] = nilai


fig = plt.figure(figsize=(10, 7))

ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(
    X, Y, Z,
    cmap="viridis",
    edgecolor="none"
)

ax.set_title("Decision Surface Sistem Urgensi Helpdesk TI")
ax.set_xlabel("Waktu Respons (Jam)")
ax.set_ylabel("Tingkat Dampak (%)")
ax.set_zlabel("Tingkat Urgensi")

plt.savefig("decision_surface.png")
plt.show()


print("\nSemua proses berhasil dijalankan!")
print("Grafik tersimpan sebagai:")
print("- grafik_agregasi.png")
print("- decision_surface.png")
