import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# FUNGSI KEANGGOTAAN TRAPESIUM
# ==========================================================

def trapesium(x, a, b, c, d):
    if x <= a:
        return 0.0
    elif a < x <= b:
        return 1.0
    elif b < x < c:
        return (c - x) / (c - b)
    elif c <= x < d:
        return (d - x) / (d - c)
    else:
        return 0.0


# ==========================================================
# FUNGSI KEANGGOTAAN SEGITIGA
# ==========================================================

def segitiga(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


# ==========================================================
# FUNGSI KEANGGOTAAN WAKTU RESPONS
# ==========================================================

def waktu_respons(x):

    return {
        "Cepat": trapesium(x, 0, 0, 2, 4),
        "Sedang": segitiga(x, 2, 5, 8),
        "Lambat": trapesium(x, 6, 8, 10, 10)
    }


# ==========================================================
# FUNGSI KEANGGOTAAN TINGKAT DAMPAK
# ==========================================================

def tingkat_dampak(x):

    return {
        "Rendah": trapesium(x, 0, 0, 20, 40),
        "Sedang": segitiga(x, 30, 50, 70),
        "Tinggi": trapesium(x, 60, 80, 100, 100)
    }


# ==========================================================
# FUNGSI KEANGGOTAAN OUTPUT URGENSI
# ==========================================================

def tingkat_urgensi(x):

    return {
        "Rendah": trapesium(x, 0, 0, 20, 40),
        "Sedang": segitiga(x, 30, 50, 70),
        "Tinggi": trapesium(x, 60, 80, 100, 100)
    }


# ==========================================================
# FUNGSI FUZZIFIKASI
# ==========================================================

def fuzzifikasi(input_dict):

    waktu = input_dict["waktu_respons"]
    dampak = input_dict["tingkat_dampak"]

    hasil = {
        "Waktu Respons": waktu_respons(waktu),
        "Tingkat Dampak": tingkat_dampak(dampak)
    }

    return hasil


# ==========================================================
# FUNGSI PLOT WAKTU RESPONS
# ==========================================================

def plot_waktu_respons():

    x = np.linspace(0, 10, 500)

    cepat = [waktu_respons(i)["Cepat"] for i in x]
    sedang = [waktu_respons(i)["Sedang"] for i in x]
    lambat = [waktu_respons(i)["Lambat"] for i in x]

    plt.figure(figsize=(8, 5))

    plt.plot(x, cepat, label="Cepat")
    plt.plot(x, sedang, label="Sedang")
    plt.plot(x, lambat, label="Lambat")

    plt.title("Fungsi Keanggotaan Waktu Respons")
    plt.xlabel("Waktu Respons (jam)")
    plt.ylabel("Derajat Keanggotaan")
    plt.legend()
    plt.grid(True)

    plt.savefig("waktu_respons.png")
    plt.show()


# ==========================================================
# FUNGSI PLOT TINGKAT DAMPAK
# ==========================================================

def plot_tingkat_dampak():

    x = np.linspace(0, 100, 500)

    rendah = [tingkat_dampak(i)["Rendah"] for i in x]
    sedang = [tingkat_dampak(i)["Sedang"] for i in x]
    tinggi = [tingkat_dampak(i)["Tinggi"] for i in x]

    plt.figure(figsize=(8, 5))

    plt.plot(x, rendah, label="Rendah")
    plt.plot(x, sedang, label="Sedang")
    plt.plot(x, tinggi, label="Tinggi")

    plt.title("Fungsi Keanggotaan Tingkat Dampak")
    plt.xlabel("Tingkat Dampak (%)")
    plt.ylabel("Derajat Keanggotaan")
    plt.legend()
    plt.grid(True)

    plt.savefig("tingkat_dampak.png")
    plt.show()


# ==========================================================
# FUNGSI PLOT TINGKAT URGENSI
# ==========================================================

def plot_tingkat_urgensi():

    x = np.linspace(0, 100, 500)

    rendah = [tingkat_urgensi(i)["Rendah"] for i in x]
    sedang = [tingkat_urgensi(i)["Sedang"] for i in x]
    tinggi = [tingkat_urgensi(i)["Tinggi"] for i in x]

    plt.figure(figsize=(8, 5))

    plt.plot(x, rendah, label="Rendah")
    plt.plot(x, sedang, label="Sedang")
    plt.plot(x, tinggi, label="Tinggi")

    plt.title("Fungsi Keanggotaan Tingkat Urgensi Tiket")
    plt.xlabel("Tingkat Urgensi")
    plt.ylabel("Derajat Keanggotaan")
    plt.legend()
    plt.grid(True)

    plt.savefig("tingkat_urgensi.png")
    plt.show()


# ==========================================================
# PENGUJIAN
# ==========================================================

data_uji = [
    {
        "kasus": "Ekstrem Bawah",
        "waktu_respons": 0,
        "tingkat_dampak": 0
    },
    {
        "kasus": "Kondisi Cepat",
        "waktu_respons": 2,
        "tingkat_dampak": 20
    },
    {
        "kasus": "Kondisi Transisi",
        "waktu_respons": 5,
        "tingkat_dampak": 50
    },
    {
        "kasus": "Kondisi Tinggi",
        "waktu_respons": 8,
        "tingkat_dampak": 80
    },
    {
        "kasus": "Ekstrem Atas",
        "waktu_respons": 10,
        "tingkat_dampak": 100
    }
]


# ==========================================================
# MENAMPILKAN HASIL FUZZIFIKASI
# ==========================================================

for data in data_uji:

    hasil = fuzzifikasi({
        "waktu_respons": data["waktu_respons"],
        "tingkat_dampak": data["tingkat_dampak"]
    })

    print("\n======================================")
    print(data["kasus"])
    print("======================================")

    print("Waktu Respons:")
    for label, nilai in hasil["Waktu Respons"].items():
        print(f"  {label}: {nilai:.2f}")

    print("Tingkat Dampak:")
    for label, nilai in hasil["Tingkat Dampak"].items():
        print(f"  {label}: {nilai:.2f}")


# ==========================================================
# MENYIMPAN GRAFIK
# ==========================================================

plot_waktu_respons()
plot_tingkat_dampak()
plot_tingkat_urgensi()