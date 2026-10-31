
import numpy as np


# ==================================================
# 1. FUNGSI KEANGGOTAAN
# ==================================================

def trimf(x, params):
    a, b, c = params
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)

    if b > a:
        idx = (x >= a) & (x <= b)
        y[idx] = (x[idx] - a) / (b - a)

    if c > b:
        idx = (x > b) & (x <= c)
        y[idx] = (c - x[idx]) / (c - b)

    y[x == b] = 1.0
    return np.clip(y, 0, 1)


def trapmf(x, params):
    a, b, c, d = params
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)

    if b > a:
        idx = (x >= a) & (x < b)
        y[idx] = (x[idx] - a) / (b - a)

    y[(x >= b) & (x <= c)] = 1.0

    if d > c:
        idx = (x > c) & (x <= d)
        y[idx] = (d - x[idx]) / (d - c)

    return np.clip(y, 0, 1)


# ==================================================
# 2. KELAS FUZZY INFERENCE SYSTEM
# ==================================================

class FuzzyInferenceSystem:

    def __init__(self):
        self.inputs = {}
        self.output = None
        self.rules = []

    def add_input_variable(self, name, universe, mf_dict):
        self.inputs[name] = {
            "universe": np.asarray(universe, dtype=float),
            "mf": mf_dict
        }

    def set_output_variable(self, name, universe, mf_dict):
        self.output = {
            "name": name,
            "universe": np.asarray(universe, dtype=float),
            "mf": mf_dict
        }

    def add_rule(self, rule_tuple):
        self.rules.append(rule_tuple)

    def compute(self, input_values_dict):
        if self.output is None or not self.rules:
            raise ValueError("Output atau aturan fuzzy belum dibuat.")

        if set(input_values_dict) != set(self.inputs):
            raise ValueError("Input tidak sesuai variabel yang terdaftar.")

        # Fuzzifikasi
        fuzzified = {}

        for name, value in input_values_dict.items():
            var = self.inputs[name]
            universe = var["universe"]

            if not np.isfinite(value):
                raise ValueError(f"Input {name} tidak valid.")

            if value < universe[0] or value > universe[-1]:
                raise ValueError(f"Input {name} di luar domain.")

            fuzzified[name] = {
                label: float(np.interp(value, universe, mf))
                for label, mf in var["mf"].items()
            }

        # Evaluasi aturan, implikasi, dan agregasi
        z = self.output["universe"]
        aggregated = np.zeros_like(z)

        for antecedents, consequent in self.rules:
            alpha = min(
                fuzzified[var_name][label]
                for var_name, label in antecedents
            )

            output_mf = self.output["mf"][consequent]
            implied = np.minimum(alpha, output_mf)
            aggregated = np.maximum(aggregated, implied)

        # Defuzzifikasi centroid
        area = np.trapezoid(aggregated, z)

        if area <= 0:
            raise ValueError(
                "Tidak ada aturan aktif. Periksa fungsi keanggotaan "
                "dan basis aturan."
            )

        crisp = np.trapezoid(z * aggregated, z) / area
        return crisp


# ==================================================
# 3. DOMAIN DAN FUNGSI KEANGGOTAAN INPUT
# ==================================================

# Lama langganan: 0-24 bulan
x1 = np.linspace(0, 24, 241)

mf_lama = {
    "Baru": trapmf(x1, [0, 0, 3, 12]),
    "Lama": trapmf(x1, [6, 12, 24, 24])
}

# Frekuensi transaksi: 0-15 kali per bulan
x2 = np.linspace(0, 15, 151)

mf_frekuensi = {
    "Jarang": trapmf(x2, [0, 0, 2, 8]),
    "Sering": trapmf(x2, [5, 10, 15, 15])
}

# Diskon: 0-30 persen
z = np.linspace(0, 30, 301)

mf_diskon = {
    "Kecil": trimf(z, [0, 5, 12]),
    "Sedang": trimf(z, [8, 15, 22]),
    "Besar": trimf(z, [18, 25, 30])
}


# ==================================================
# 4. MEMBANGUN SISTEM DAN BASIS ATURAN
# ==================================================

fis = FuzzyInferenceSystem()

fis.add_input_variable("lama", x1, mf_lama)
fis.add_input_variable("frekuensi", x2, mf_frekuensi)
fis.set_output_variable("diskon", z, mf_diskon)

fis.add_rule((
    [("lama", "Baru"), ("frekuensi", "Jarang")],
    "Kecil"
))

fis.add_rule((
    [("lama", "Baru"), ("frekuensi", "Sering")],
    "Sedang"
))

fis.add_rule((
    [("lama", "Lama"), ("frekuensi", "Jarang")],
    "Sedang"
))

fis.add_rule((
    [("lama", "Lama"), ("frekuensi", "Sering")],
    "Besar"
))


# ==================================================
# 5. PENGUJIAN TIGA KASUS
# ==================================================

kasus = [
    {"lama": 3, "frekuensi": 2},
    {"lama": 12, "frekuensi": 6},
    {"lama": 24, "frekuensi": 15}
]

for i, data in enumerate(kasus, start=1):
    diskon = fis.compute(data)

    print(f"Kasus {i}")
    print(f"Lama langganan: {data['lama']} bulan")
    print(f"Frekuensi transaksi: {data['frekuensi']} kali/bulan")
    print(f"Rekomendasi diskon: {diskon:.2f}%")
    print("-" * 35)
