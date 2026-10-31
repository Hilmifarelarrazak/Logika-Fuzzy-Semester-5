
# ==========================================
# SISTEM KENDALI KIPAS PENDINGIN SERVER
# PRAKTIKUM 6 - FUZZY RULE
# ==========================================

# 1. DATA INPUT FUZZY

suhu = {
    "Dingin": 0.2,
    "Normal": 0.8,
    "Panas": 0.0
}

cpu = {
    "Ringan": 0.0,
    "Sedang": 0.5,
    "Berat": 0.5
}


# 2. BASIS ATURAN FUZZY

rules = [
    ("Dingin", "Ringan", "Lambat"),
    ("Dingin", "Sedang", "Lambat"),
    ("Dingin", "Berat", "Sedang"),
    ("Normal", "Ringan", "Lambat"),
    ("Normal", "Sedang", "Sedang"),
    ("Normal", "Berat", "Cepat"),
    ("Panas", "Ringan", "Sedang"),
    ("Panas", "Sedang", "Cepat"),
    ("Panas", "Berat", "Cepat")
]


# 3. EVALUASI ATURAN FUZZY

print("======================================")
print(" SISTEM KENDALI KIPAS SERVER")
print("======================================")

print("\nINPUT SUHU RUANG:")
for label, nilai in suhu.items():
    print(f"{label:10} : {nilai}")

print("\nINPUT BEBAN CPU:")
for label, nilai in cpu.items():
    print(f"{label:10} : {nilai}")

print("\nHASIL EVALUASI ATURAN FUZZY")
print("--------------------------------------")

aktif = 0

for i, (s, c, output) in enumerate(rules, start=1):

    # Menghitung firing strength menggunakan MIN
    alpha = min(suhu[s], cpu[c])

    print(f"Rule {i}:")
    print(f"IF Suhu {s} AND CPU {c}")
    print(f"THEN Kipas {output}")
    print(f"Firing Strength (alpha) = {alpha:.2f}")

    if alpha > 0:
        print("Status: AKTIF")
        aktif += 1
    else:
        print("Status: TIDAK AKTIF")

    print("--------------------------------------")

print(f"\nJumlah aturan aktif: {aktif} dari 9 aturan")
print("Evaluasi aturan selesai.")
