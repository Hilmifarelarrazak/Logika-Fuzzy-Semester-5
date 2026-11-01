def fungsi_bayi(x):
    if x <= 5:
        return 1
    elif 5 < x < 6:
        return 6 - x
    else:
        return 0


def fungsi_anak(x):
    if x <= 5:
        return 0
    elif 5 < x < 6:
        return x - 5
    elif 6 <= x <= 11:
        return 1
    elif 11 < x < 12:
        return 12 - x
    else:
        return 0


def fungsi_remaja(x):
    if x <= 9:
        return 0
    elif 9 < x < 10:
        return x - 9
    elif 10 <= x <= 19:
        return 1
    elif 19 < x < 20:
        return 20 - x
    else:
        return 0


def fungsi_pemuda(x):
    if x <= 14:
        return 0
    elif 14 < x < 15:
        return x - 14
    elif 15 <= x <= 24:
        return 1
    elif 24 < x < 25:
        return 25 - x
    else:
        return 0


def fungsi_dewasa(x):
    if x <= 19:
        return 0
    elif 19 < x < 20:
        return x - 19
    elif 20 <= x <= 65:
        return 1
    elif 65 < x < 66:
        return 66 - x
    else:
        return 0


def fungsi_lansia(x):
    if x <= 64:
        return 0
    elif 64 < x < 65:
        return x - 64
    elif 65 <= x <= 150:
        return 1
    else:
        return 0


# Contoh pengujian fungsi keanggotaan

print("Bayi   :", fungsi_bayi(5.5))
print("Anak   :", fungsi_anak(5.5))
print("Remaja :", fungsi_remaja(9.5))
print("Pemuda :", fungsi_pemuda(14.5))
print("Dewasa :", fungsi_dewasa(19.5))
print("Lansia :", fungsi_lansia(64.5))