import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# 1. Semesta pembicaraan
z = np.arange(0, 101, 1)

# 2. Fungsi keanggotaan output
jelek = fuzz.trapmf(z, [0, 0, 25, 45])
sedang = fuzz.trimf(z, [35, 55, 75])
bagus = fuzz.trapmf(z, [65, 85, 100, 100])

# 3. Nilai firing strength
alpha_jelek = 0.5
alpha_sedang = 0.8
alpha_bagus = 0.2

# 4. Implikasi Mamdani menggunakan MIN
potong_jelek = np.fmin(alpha_jelek, jelek)
potong_sedang = np.fmin(alpha_sedang, sedang)
potong_bagus = np.fmin(alpha_bagus, bagus)

# 5. Agregasi menggunakan MAX
agregasi = np.fmax(
    np.fmax(potong_jelek, potong_sedang),
    potong_bagus
)

# 6. Defuzzifikasi lima metode
metode = ['centroid', 'bisector', 'mom', 'som', 'lom']

hasil = {}

for m in metode:
    hasil[m] = fuzz.defuzz(z, agregasi, m)

# 7. Menampilkan hasil
print("HASIL DEFUZZIFIKASI KUALITAS WIFI")
print("---------------------------------")

for m, nilai in hasil.items():
    print(f"{m.upper():10s}: {nilai:.2f}")

# 8. Membuat satu grafik
plt.figure(figsize=(12, 6))

plt.plot(z, jelek, '--', label='Jelek')
plt.plot(z, sedang, '--', label='Sedang')
plt.plot(z, bagus, '--', label='Bagus')

plt.fill_between(
    z, 0, agregasi,
    color='skyblue',
    alpha=0.4,
    label='Agregasi Fuzzy'
)

plt.plot(
    z, agregasi,
    color='blue',
    linewidth=2.5,
    label='Kurva Agregasi'
)

warna = {
    'centroid': 'red',
    'bisector': 'purple',
    'mom': 'black',
    'som': 'green',
    'lom': 'orange'
}

for m, nilai in hasil.items():
    plt.axvline(
        nilai,
        color=warna[m],
        linestyle='--',
        linewidth=2,
        label=f'{m.upper()} ({nilai:.2f})'
    )

plt.title('Komparasi 5 Metode Defuzzifikasi Kualitas WiFi')
plt.xlabel('Kualitas Sinyal WiFi (Skala 0-100)')
plt.ylabel('Derajat Keanggotaan')
plt.xlim(0, 100)
plt.ylim(0, 1.05)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig('grafik_defuzzifikasi_wifi.png', dpi=300)
plt.show()