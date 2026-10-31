import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. FUNGSI KEANGGOTAAN
# ==========================================

def trapezoid(x, a, b, c, d):
    x = np.asarray(x, dtype=float)

    if a == b:
        left = np.where(x >= b, 1.0, 0.0)
    else:
        left = np.where(
            x <= a, 0.0,
            np.minimum(1.0, (x-a)/(b-a))
        )

    if c == d:
        right = np.where(x <= c, 1.0, 0.0)
    else:
        right = np.where(
            x >= d, 0.0,
            np.minimum(1.0, (d-x)/(d-c))
        )

    return np.maximum(0, np.minimum(left, right))


def triangle(x, a, b, c):
    x = np.asarray(x, dtype=float)

    return np.maximum(
        0,
        np.minimum(
            np.where(
                x <= b,
                (x-a)/(b-a),
                (c-x)/(c-b)
            ),
            1
        )
    )


# ==========================================
# 2. FUZZIFIKASI WAKTU RESPONS
# ==========================================

def fuzzy_waktu(x):
    return {
        "Cepat": trapezoid(x, 0, 0, 2, 4),
        "Sedang": triangle(x, 2, 5, 8),
        "Lambat": trapezoid(x, 6, 8, 10, 10)
    }


# ==========================================
# 3. FUZZIFIKASI TINGKAT DAMPAK
# ==========================================

def fuzzy_dampak(x):
    return {
        "Rendah": trapezoid(x, 0, 0, 20, 40),
        "Sedang": triangle(x, 30, 50, 70),
        "Tinggi": trapezoid(x, 60, 80, 100, 100)
    }


# ==========================================
# 4. FUNGSI KEANGGOTAAN OUTPUT
# ==========================================

def fuzzy_output(z):
    return {
        "Rendah": trapezoid(z, 0, 0, 20, 40),
        "Sedang": triangle(z, 30, 50, 70),
        "Tinggi": trapezoid(z, 60, 80, 100, 100)
    }


# ==========================================
# 5. BASIS ATURAN FUZZY
# ==========================================

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


# ==========================================
# 6. MESIN INFERENSI MAMDANI
# ==========================================

def evaluasi_sistem_fuzzy(waktu, dampak):

    mu_waktu = fuzzy_waktu(waktu)
    mu_dampak = fuzzy_dampak(dampak)

    z = np.linspace(0, 100, 1001)
    mu_output = fuzzy_output(z)

    hasil_agregasi = np.zeros_like(z)

    # Proses inferensi dan agregasi
    for input_waktu, input_dampak, output in aturan:

        alpha = min(
            mu_waktu[input_waktu],
            mu_dampak[input_dampak]
        )

        hasil_implikasi = np.minimum(
            alpha,
            mu_output[output]
        )

        hasil_agregasi = np.maximum(
            hasil_agregasi,
            hasil_implikasi
        )

    # Defuzzifikasi metode Centroid
    luas = np.sum(hasil_agregasi)

    if luas == 0:
        nilai_urgensi = 0
    else:
        nilai_urgensi = (
            np.sum(z * hasil_agregasi) / luas
        )

    # Menentukan kategori berdasarkan
    # derajat keanggotaan terbesar
    mu_hasil = fuzzy_output(nilai_urgensi)

    kategori = max(
        mu_hasil,
        key=mu_hasil.get
    )

    return nilai_urgensi, kategori, z, hasil_agregasi


# ==========================================
# 7. PENGUJIAN 5 SKENARIO
# ==========================================

data_uji = [
    (1, 10),
    (3, 35),
    (5, 50),
    (7, 75),
    (9, 95)
]

print("HASIL PENGUJIAN SISTEM FUZZY MAMDANI")
print("=" * 75)

print(
    f"{'No':<5}{'Waktu':<12}{'Dampak':<12}"
    f"{'Urgensi':<15}{'Kategori'}"
)

print("-" * 75)

for i, (waktu, dampak) in enumerate(data_uji, 1):

    hasil, kategori, z, agregasi = (
        evaluasi_sistem_fuzzy(waktu, dampak)
    )

    print(
        f"{i:<5}{waktu:<12}{dampak:<12}"
        f"{hasil:<15.2f}{kategori}"
    )


# ==========================================
# 8. GRAFIK AGREGASI OUTPUT
# ==========================================

waktu = 5
dampak = 50

hasil, kategori, z, agregasi = (
    evaluasi_sistem_fuzzy(waktu, dampak)
)

plt.figure(figsize=(9, 5))

plt.plot(z, agregasi, label="Hasil Agregasi")
plt.axvline(
    hasil,
    linestyle="--",
    label=f"Centroid = {hasil:.2f}"
)

plt.title("Agregasi Tingkat Urgensi Tiket")
plt.xlabel("Tingkat Urgensi")
plt.ylabel("Derajat Keanggotaan")
plt.legend()
plt.grid()

plt.savefig("grafik_agregasi.png", dpi=300)
plt.show()


# ==========================================
# 9. DECISION SURFACE PLOT 3D
# ==========================================

waktu_range = np.linspace(0, 10, 30)
dampak_range = np.linspace(0, 100, 30)

X, Y = np.meshgrid(waktu_range, dampak_range)

Z = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):

        hasil, kategori, _, _ = (
            evaluasi_sistem_fuzzy(
                X[i, j],
                Y[i, j]
            )
        )

        Z[i, j] = hasil


fig = plt.figure(figsize=(10, 7))

ax = fig.add_subplot(111, projection="3d")

surf = ax.plot_surface(
    X, Y, Z,
    cmap="viridis",
    edgecolor="none",
    alpha=0.9
)

ax.set_xlabel("Waktu Respons (Jam)")
ax.set_ylabel("Tingkat Dampak (%)")
ax.set_zlabel("Tingkat Urgensi")

ax.set_title(
    "Decision Surface Plot Sistem Urgensi Tiket Helpdesk"
)

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.savefig("decision_surface.png", dpi=300)

plt.show()