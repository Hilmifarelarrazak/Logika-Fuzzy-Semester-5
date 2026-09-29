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
    return 6 - x


# ==========================================================
# 3. FUNGSI KEANGGOTAAN ANAK
# ==========================================================

def trapesium_up_anak(x):
    return x - 5


def trapesium_down_anak(x):
    return 12 - x


# ==========================================================
# 4. FUNGSI KEANGGOTAAN REMAJA
# ==========================================================

def trapesium_up_remaja(x):
    return x - 9


def trapesium_down_remaja(x):
    return 20 - x


# ==========================================================
# 5. FUNGSI KEANGGOTAAN PEMUDA
# ==========================================================

def trapesium_up_pemuda(x):
    return x - 14


def trapesium_down_pemuda(x):
    return 25 - x


# ==========================================================
# 6. FUNGSI KEANGGOTAAN DEWASA
# ==========================================================

def trapesium_up_dewasa(x):
    return x - 19


def trapesium_down_dewasa(x):
    return 66 - x


# ==========================================================
# 7. FUNGSI KEANGGOTAAN LANSIA
# ==========================================================

def trapesium_up_lansia(x):
    return x - 64


# ==========================================================
# 8. DAFTAR FUNGSI
# ==========================================================

fungsi = {

    "trapesium_down_bayi": trapesium_down_bayi,

    "trapesium_up_anak": trapesium_up_anak,
    "trapesium_down_anak": trapesium_down_anak,

    "trapesium_up_remaja": trapesium_up_remaja,
    "trapesium_down_remaja": trapesium_down_remaja,

    "trapesium_up_pemuda": trapesium_up_pemuda,
    "trapesium_down_pemuda": trapesium_down_pemuda,

    "trapesium_up_dewasa": trapesium_up_dewasa,
    "trapesium_down_dewasa": trapesium_down_dewasa,

    "trapesium_up_lansia": trapesium_up_lansia
}


# ==========================================================
# 9. DAFTAR TABEL DATABASE
# ==========================================================

tabel_kategori = {

    "Bayi": "tb_domain_usia_bayi",
    "Anak": "tb_domain_usia_anak",
    "Remaja": "tb_domain_usia_remaja",
    "Pemuda": "tb_domain_usia_pemuda",
    "Dewasa": "tb_domain_usia_dewasa",
    "Lansia": "tb_domain_usia_lansia"
}


# ==========================================================
# 10. FUNGSI FUZZIFIKASI
# ==========================================================

def fuzzifikasi_usia(x, kategori):

    cursor = db.cursor()

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

    # Jika usia tidak ditemukan
    if not data:
        return 0

    nilai_maksimum = 0

    # Mengecek setiap fungsi
    for batas_bawah, batas_atas, nama_fungsi in data:

        # ------------------------------------------
        # Fungsi bernilai 0
        # ------------------------------------------

        if nama_fungsi == "0":

            nilai = 0

        # ------------------------------------------
        # Fungsi bernilai 1
        # ------------------------------------------

        elif nama_fungsi == "1":

            nilai = 1

        # ------------------------------------------
        # Fungsi trapesium
        # ------------------------------------------

        elif nama_fungsi in fungsi:

            fungsi_y = fungsi[nama_fungsi]

            nilai = fungsi_y(x)

        else:

            raise ValueError(
                f"Fungsi '{nama_fungsi}' belum dibuat di Python."
            )

        # ------------------------------------------
        # Membatasi nilai 0 sampai 1
        # ------------------------------------------

        nilai = max(0, min(1, nilai))

        # ------------------------------------------
        # Mengambil nilai terbesar
        # ------------------------------------------

        if nilai > nilai_maksimum:

            nilai_maksimum = nilai

    return nilai_maksimum


# ==========================================================
# 11. INPUT USIA
# ==========================================================

usia = float(input("Masukkan usia: "))


# ==========================================================
# 12. VALIDASI USIA
# ==========================================================

if usia < 0 or usia > 150:

    print()
    print("Usia harus berada pada domain 0 sampai 150 tahun.")

else:

    # ======================================================
    # 13. PROSES FUZZIFIKASI
    # ======================================================

    hasil = {}

    for kategori in tabel_kategori:

        nilai = fuzzifikasi_usia(
            usia,
            kategori
        )

        hasil[kategori] = nilai


    # ======================================================
    # 14. MENAMPILKAN HASIL
    # ======================================================

    print()
    print("========================================")
    print("          HASIL FUZZIFIKASI USIA")
    print("========================================")

    print(f"Usia : {usia}")

    print("----------------------------------------")

    for kategori, nilai in hasil.items():

        print(
            f"{kategori:10} : {nilai:.2f}"
        )

    print("----------------------------------------")


# ==========================================================
# 15. MENUTUP DATABASE
# ==========================================================

db.close()