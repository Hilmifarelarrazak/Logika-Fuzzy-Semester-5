import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# 1. FUNGSI CRISP
# ==========================================================

def crisp_memuaskan(rating, threshold=4.0):
    """
    Fungsi Crisp.

    Jika rating >= 4 maka nilai = 1
    Jika rating < 4 maka nilai = 0
    """
    return np.where(rating >= threshold, 1.0, 0.0)


# ==========================================================
# 2. FUNGSI FUZZY LINEAR NAIK
# ==========================================================

def fuzzy_memuaskan(rating, a=2.5, b=4.5):
    """
    Fungsi keanggotaan Fuzzy Linear Naik.

    x <= a       -> 0
    a < x < b    -> (x-a)/(b-a)
    x >= b       -> 1
    """

    derajat = (rating - a) / (b - a)

    # Membatasi nilai antara 0 dan 1
    return np.clip(derajat, 0.0, 1.0)


# ==========================================================
# 3. MEMBUAT DOMAIN RATING
# ==========================================================

# Rating pengguna dari 1 sampai 5
ratings = np.linspace(1.0, 5.0, 500)


# ==========================================================
# 4. MENGHITUNG NILAI KEANGGOTAAN
# ==========================================================

y_crisp = crisp_memuaskan(
    ratings,
    threshold=4.0
)

y_fuzzy = fuzzy_memuaskan(
    ratings,
    a=2.5,
    b=4.5
)


# ==========================================================
# 5. MENAMPILKAN BEBERAPA NILAI
# ==========================================================

print("==============================================================")
print("        PERBANDINGAN NILAI CRISP DAN FUZZY")
print("==============================================================")

rating_uji = [
    1.0,
    2.0,
    2.5,
    3.0,
    3.5,
    4.0,
    4.5,
    5.0
]

for x in rating_uji:

    crisp = float(
        crisp_memuaskan(
            x,
            threshold=4.0
        )
    )

    fuzzy = float(
        fuzzy_memuaskan(
            x,
            a=2.5,
            b=4.5
        )
    )

    print(f"\nRating = {x}")
    print(f"  Crisp        : {crisp:.3f}")
    print(f"  Fuzzy mu(x)  : {fuzzy:.3f}")


# ==========================================================
# 6. PENGUJIAN DI SEKITAR RATING 4.0
# ==========================================================

test_values = [
    3.8,
    3.9,
    3.99,
    4.0,
    4.01,
    4.2
]

print("\n")
print("==========================================================================")
print("        PENGUJIAN DI SEKITAR THRESHOLD CRISP = 4.0")
print("==========================================================================")

print(
    f"{'Rating':<8} | "
    f"{'Crisp':<8} | "
    f"{'Fuzzy mu(x)':<12} | "
    f"{'Interpretasi Fuzzy'}"
)

print("-" * 75)

for val in test_values:

    # Nilai Crisp
    c_val = float(
        crisp_memuaskan(
            val,
            threshold=4.0
        )
    )

    # Nilai Fuzzy
    f_val = float(
        fuzzy_memuaskan(
            val,
            a=2.5,
            b=4.5
        )
    )

    # Interpretasi fuzzy
    interpretasi = (
        f"Tingkat pemenuhan {f_val * 100:.1f}%"
    )

    print(
        f"{val:<8.2f} | "
        f"{c_val:<8.1f} | "
        f"{f_val:<12.3f} | "
        f"{interpretasi}"
    )


# ==========================================================
# 7. MEMBUAT GRAFIK
# ==========================================================

plt.figure(figsize=(11, 6))


# ----------------------------------------------------------
# Kurva Crisp
# ----------------------------------------------------------

plt.step(
    ratings,
    y_crisp,
    label="Crisp (Threshold = 4.0)",
    linewidth=2.5,
    where="post"
)


# ----------------------------------------------------------
# Kurva Fuzzy Linear Naik
# ----------------------------------------------------------

plt.plot(
    ratings,
    y_fuzzy,
    label="Fuzzy Linear Naik [2.5, 4.5]",
    linewidth=2.5
)


# ==========================================================
# 8. PENANDA TITIK PENTING
# ==========================================================

# Garis threshold Crisp
plt.axvline(
    x=4.0,
    linestyle="--",
    alpha=0.6,
    label="Threshold Crisp = 4.0"
)

# Batas awal fuzzy
plt.axvline(
    x=2.5,
    linestyle=":",
    alpha=0.6,
    label="Awal Fuzzy = 2.5"
)

# Batas akhir fuzzy
plt.axvline(
    x=4.5,
    linestyle=":",
    alpha=0.6,
    label="Akhir Fuzzy = 4.5"
)


# ==========================================================
# 9. JUDUL DAN LABEL
# ==========================================================

plt.title(
    "Perbandingan Crisp dan Fuzzy Linear Naik",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel(
    "Rating Pengguna (Skala 1 - 5)",
    fontsize=11
)

plt.ylabel(
    "Derajat Keanggotaan / Nilai Kebenaran",
    fontsize=11
)


# ==========================================================
# 10. PENGATURAN SUMBU
# ==========================================================

plt.xlim(
    1.0,
    5.0
)

plt.ylim(
    -0.05,
    1.1
)

plt.xticks(
    np.arange(
        1.0,
        5.1,
        0.5
    )
)

plt.yticks(
    np.arange(
        0.0,
        1.1,
        0.1
    )
)


# ==========================================================
# 11. GRID DAN LEGEND
# ==========================================================

plt.grid(
    True,
    linestyle=":",
    alpha=0.6
)

plt.legend(
    loc="upper left",
    fontsize=9
)

plt.tight_layout()


# ==========================================================
# 12. SIMPAN GRAFIK
# ==========================================================

plt.savefig(
    "perbandingan_crisp_fuzzy.png",
    dpi=300
)


# ==========================================================
# 13. TAMPILKAN GRAFIK
# ==========================================================

plt.show()
