import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# 1. Semesta pembicaraan
z = np.arange(0, 101, 1)

# 2. Fungsi keanggotaan output diskon
kecil = fuzz.trapmf(z, [0, 0, 20, 40])
sedang = fuzz.trimf(z, [30, 50, 70])
besar = fuzz.trapmf(z, [60, 80, 100, 100])

# 3. Nilai firing strength output
alpha_kecil = 0.2
alpha_sedang = 0.5
alpha_besar = 0.5

# 4. Implikasi Mamdani menggunakan MIN
potong_kecil = np.fmin(alpha_kecil, kecil)
potong_sedang = np.fmin(alpha_sedang, sedang)
potong_besar = np.fmin(alpha_besar, besar)

# 5. Agregasi menggunakan MAX
agregasi = np.fmax(
    np.fmax(potong_kecil, potong_sedang),
    potong_besar
)

# 6. Defuzzifikasi lima metode
metode = ['centroid', 'bisector', 'mom', 'som', 'lom']

hasil = {}

for m in metode:
    hasil[m] = fuzz.defuzz(z, agregasi, m)

# 7. Menampilkan hasil
print("HASIL DEFUZZIFIKASI SISTEM DISKON TOKO")
print("--------------------------------------")

for m, nilai in hasil.items():
    print(f"{m.upper():10s}: {nilai:.2f}%")

# 8. Membuat satu grafik
plt.figure(figsize=(12, 6))

plt.plot(z, kecil, '--', label='Diskon Kecil')
plt.plot(z, sedang, '--', label='Diskon Sedang')
plt.plot(z, besar, '--', label='Diskon Besar')

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
        label=f'{m.upper()} ({nilai:.2f}%)'
    )

plt.title('Komparasi 5 Metode Defuzzifikasi Diskon Toko')
plt.xlabel('Besar Diskon (%)')
plt.ylabel('Derajat Keanggotaan')
plt.xlim(0, 100)
plt.ylim(0, 1.05)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig('grafik_defuzzifikasi_diskon.png', dpi=300)
plt.show()
