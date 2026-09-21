import mysql.connector


# ==========================================================
# 1. KONEKSI DATABASE
# ==========================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="logika_fuzzy"
)

print("Koneksi database berhasil!")


# ==========================================================
# 2. FUNGSI KEANGGOTAAN BAYI
# ==========================================================

def trapesium_down_bayi(x):
    """
    Fungsi keanggotaan Bayi bagian turun.

    Domain:
    5 < x < 6

    Persamaan:
    μ(x) = 6 - x
    """
    return 6 - x


# ==========================================================
# 3. FUNGSI KEANGGOTAAN ANAK
# ==========================================================

def trapesium_up_anak(x):
    """
    Fungsi keanggotaan Anak bagian naik.

    Domain:
    5 < x < 6

    Persamaan:
    μ(x) = x - 5
    """
    return x - 5


def trapesium_down_anak(x):
    """
    Fungsi keanggotaan Anak bagian turun.

    Domain:
    11 < x < 12

    Persamaan:
    μ(x) = 12 - x
    """
    return 12 - x


# ==========================================================
# 4. FUNGSI KEANGGOTAAN REMAJA
# ==========================================================

def trapesium_up_remaja(x):
    """
    Fungsi keanggotaan Remaja bagian naik.

    Domain:
    9 < x < 10

    Persamaan:
    μ(x) = x - 9
    """
    return x - 9


def trapesium_down_remaja(x):
    """
    Fungsi keanggotaan Remaja bagian turun.

    Domain:
    19 < x < 20

    Persamaan:
    μ(x) = 20 - x
    """
    return 20 - x


# ==========================================================
# 5. FUNGSI KEANGGOTAAN PEMUDA
# ==========================================================

def trapesium_up_pemuda(x):
    """
    Fungsi keanggotaan Pemuda bagian naik.

    Domain:
    14 < x < 15

    Persamaan:
    μ(x) = x - 14
    """
    return x - 14


def trapesium_down_pemuda(x):
    """
    Fungsi keanggotaan Pemuda bagian turun.

    Domain:
    24 < x < 25

    Persamaan:
    μ(x) = 25 - x
    """
    return 25 - x


# ==========================================================
# 6. FUNGSI KEANGGOTAAN DEWASA
# ==========================================================

def trapesium_up_dewasa(x):
    """
    Fungsi keanggotaan Dewasa bagian naik.

    Domain:
    19 < x < 20

    Persamaan:
    μ(x) = x - 19
    """
    return x - 19


def trapesium_down_dewasa(x):
    """
    Fungsi keanggotaan Dewasa bagian turun.

    Domain:
    65 < x < 66

    Persamaan:
    μ(x) = 66 - x
    """
    return 66 - x


# ==========================================================
# 7. FUNGSI KEANGGOTAAN LANSIA
# ==========================================================

def trapesium_up_lansia(x):
    """
    Fungsi keanggotaan Lansia bagian naik.

    Domain:
    64 < x < 65

    Persamaan:
    μ(x) = x - 64
    """
    return x - 64


# ==========================================================
# 8. DAFTAR FUNGSI
# ==========================================================

fungsi = {

    "trapesium_down_bayi":
        trapesium_down_bayi,

    "trapesium_up_anak":
        trapesium_up_anak,

    "trapesium_down_anak":
        trapesium_down_anak,

    "trapesium_up_remaja":
        trapesium_up_remaja,

    "trapesium_down_remaja":
        trapesium_down_remaja,

    "trapesium_up_pemuda":
        trapesium_up_pemuda,

    "trapesium_down_pemuda":
        trapesium_down_pemuda,

    "trapesium_up_dewasa":
        trapesium_up_dewasa,

    "trapesium_down_dewasa":
        trapesium_down_dewasa,

    "trapesium_up_lansia":
        trapesium_up_lansia
}


# ==========================================================
# 9. DAFTAR TABEL
# ==========================================================

tabel_kategori = {

    "bayi": "tb_domain_usia_bayi",
    "anak": "tb_domain_usia_anak",
    "remaja": "tb_domain_usia_remaja",
    "pemuda": "tb_domain_usia_pemuda",
    "dewasa": "tb_domain_usia_dewasa",
    "lansia": "tb_domain_usia_lansia"
}


# ==========================================================
# 10. FUNGSI FUZZIFIKASI
# ==========================================================

def fuzzifikasi_usia(x, kategori):

    cursor = db.cursor()

    # Mengambil nama tabel berdasarkan kategori
    nama_tabel = tabel_kategori[kategori]

    query = f"""
        SELECT batas_bawah, batas_atas, fungsi
        FROM {nama_tabel}
        WHERE %s >= batas_bawah
        AND %s <= batas_atas
    """

    cursor.execute(query, (x, x))

    data = cursor.fetchall()

    cursor.close()

    if not data:
        return None

    # Mengecek semua interval
    for batas_bawah, batas_atas, nama_fungsi in data:

        # Jika nilai database = 0
        if nama_fungsi == "0":
            nilai = 0

        # Jika nilai database = 1
        elif nama_fungsi == "1":
            nilai = 1

        # Jika database memberikan nama fungsi
        elif nama_fungsi in fungsi:

            fungsi_y = fungsi[nama_fungsi]

            nilai = fungsi_y(x)

        else:

            raise ValueError(
                f"Fungsi '{nama_fungsi}' belum dibuat di Python."
            )

        # Memastikan nilai berada antara 0 dan 1
        nilai = max(0, min(1, nilai))

        # Karena pada titik batas bisa ada lebih dari satu interval,
        # kita ambil nilai yang paling besar
        if nilai >= 0:
            return nilai

    return None


# ==========================================================
# 11. INPUT USIA
# ==========================================================

usia = float(input("Masukkan usia: "))


# ==========================================================
# 12. PROSES FUZZIFIKASI SEMUA KATEGORI
# ==========================================================

hasil = {}

for kategori in tabel_kategori:

    nilai = fuzzifikasi_usia(usia, kategori)

    hasil[kategori] = nilai


# ==========================================================
# 13. MENAMPILKAN HASIL
# ==========================================================

print()
print("========================================")
print("        HASIL FUZZIFIKASI USIA")
print("========================================")

print(f"Usia : {usia}")

print("----------------------------------------")

for kategori, nilai in hasil.items():

    print(
        f"{kategori.capitalize():10} : {nilai}"
    )

print("----------------------------------------")


# ==========================================================
# 14. MENUTUP DATABASE
# ==========================================================

db.close()