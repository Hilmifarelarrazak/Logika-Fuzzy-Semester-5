
# ==========================================
# SISTEM PENENTUAN DISKON TOKO
# PRAKTIKUM 6 - FUZZY RULE
# ==========================================

# 1. DATA INPUT FUZZY

pembelian = {
    "Sedikit": 0.2,
    "Sedang": 0.8,
    "Banyak": 0.0
}

belanja = {
    "Jarang": 0.0,
    "Sedang": 0.5,
    "Sering": 0.5
}

# 2. BASIS ATURAN FUZZY

rules = [
    ("Sedikit", "Jarang", "Kecil"),
    ("Sedikit", "Sedang", "Kecil"),
    ("Sedikit", "Sering", "Sedang"),
    ("Sedang", "Jarang", "Kecil"),
    ("Sedang", "Sedang", "Sedang"),
    ("Sedang", "Sering", "Besar"),
    ("Banyak", "Jarang", "Sedang"),
    ("Banyak", "Sedang", "Besar"),
    ("Banyak", "Sering", "Besar")
]

# 3. EVALUASI ATURAN FUZZY

print("======================================")
print("     SISTEM PENENTUAN DISKON TOKO")
print("======================================")

print("\nINPUT JUMLAH PEMBELIAN:")
for label, nilai in pembelian.items():
    print(f"{label:10} : {nilai}")

print("\nINPUT FREKUENSI BELANJA:")
for label, nilai in belanja.items():
    print(f"{label:10} : {nilai}")

print("\nHASIL EVALUASI ATURAN FUZZY")
print("--------------------------------------")

aktif = 0

for i, (p, b, output) in enumerate(rules, start=1):

    # Menghitung firing strength menggunakan MIN
    alpha = min(pembelian[p], belanja[b])

    print(f"Rule {i}:")
    print(f"IF Pembelian {p} AND Belanja {b}")
    print(f"THEN Diskon {output}")
    print(f"Firing Strength (alpha) = {alpha:.2f}")

    if alpha > 0:
        print("Status: AKTIF")
        aktif += 1
    else:
        print("Status: TIDAK AKTIF")

    print("--------------------------------------")

print(f"\nJumlah aturan aktif: {aktif} dari 9 aturan")
print("Evaluasi aturan selesai.")
