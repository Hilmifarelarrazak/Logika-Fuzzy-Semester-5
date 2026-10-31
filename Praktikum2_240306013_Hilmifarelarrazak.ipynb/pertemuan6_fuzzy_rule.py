
def trapesium(x, a, b, c, d):
    if b <= x <= c:
        return 1.0
    elif a <= x < b:
        return (x - a) / (b - a)
    elif c < x <= d:
        return (d - x) / (d - c)
    return 0.0


# Fungsi trapesium dengan sisi tegak
def fuzzy(x, a, b, c, d):
    if a == b and x <= b:
        return 1.0 if x <= c else max(0, (d - x) / (d - c))
    if c == d and x >= c:
        return 1.0 if x >= b else max(0, (x - a) / (b - a))

    if x <= a or x >= d:
        return 0.0
    elif b <= x <= c:
        return 1.0
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (d - x) / (d - c)


# Aturan fuzzy
aturan = [
    ("R1", "sedikit", "jarang", "kecil"),
    ("R2", "sedikit", "sedang", "kecil"),
    ("R3", "sedikit", "sering", "sedang"),
    ("R4", "sedang", "jarang", "kecil"),
    ("R5", "sedang", "sedang", "sedang"),
    ("R6", "sedang", "sering", "besar"),
    ("R7", "banyak", "jarang", "sedang"),
    ("R8", "banyak", "sedang", "besar"),
    ("R9", "banyak", "sering", "besar"),
]

# Parameter jumlah belanja
belanja = {
    "sedikit": (0, 0, 200000, 300000),
    "sedang": (200000, 300000, 500000, 700000),
    "banyak": (600000, 800000, 1000000, 1000000)
}

# Parameter frekuensi belanja per bulan
frekuensi = {
    "jarang": (0, 0, 1, 3),
    "sedang": (2, 3, 6, 7),
    "sering": (6, 8, 10, 10)
}

# Input pelanggan
uang = 800000
kali = 8

# Hitung derajat keanggotaan
mu_belanja = {
    nama: fuzzy(uang, *parameter)
    for nama, parameter in belanja.items()
}

mu_frekuensi = {
    nama: fuzzy(kali, *parameter)
    for nama, parameter in frekuensi.items()
}

print("=== DERAJAT KEANGGOTAAN ===")
print("Jumlah belanja:", mu_belanja)
print("Frekuensi:", mu_frekuensi)

print("\n=== HASIL EVALUASI ATURAN ===")

for kode, kategori_belanja, kategori_frekuensi, hasil in aturan:
    alpha = min(
        mu_belanja[kategori_belanja],
        mu_frekuensi[kategori_frekuensi]
    )

    if alpha > 0:
        print(
            f"{kode}: {hasil.upper()}, "
            f"firing strength = {alpha:.2f}"
        )
