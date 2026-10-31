
import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# 1. FUNGSI KEANGGOTAAN
# ==========================================================

def trimf(x, params):
    """Fungsi keanggotaan segitiga [a, b, c]."""
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

    return np.clip(y, 0.0, 1.0)


def trapmf(x, params):
    """Fungsi keanggotaan trapesium [a, b, c, d]."""
    a, b, c, d = params
    x = np.asarray(x, dtype=float)

    y = np.zeros_like(x)

    if b > a:
        idx = (x >= a) & (x < b)
        y[idx] = (x[idx] - a) / (b - a)

    idx = (x >= b) & (x <= c)
    y[idx] = 1.0

    if d > c:
        idx = (x > c) & (x <= d)
        y[idx] = (d - x[idx]) / (d - c)

    return np.clip(y, 0.0, 1.0)


# ==========================================================
# 2. KELAS FUZZY INFERENCE SYSTEM
# ==========================================================

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
        if self.output is None:
            raise ValueError("Variabel output belum ditentukan.")

        # Validasi input
        if set(input_values_dict) != set(self.inputs):
            raise ValueError(
                "Input harus sesuai dengan variabel yang telah didaftarkan."
            )

        # Fuzzifikasi
        fuzzified = {}

        for name, value in input_values_dict.items():
            variable = self.inputs[name]

            if not np.isfinite(value):
                raise ValueError(f"Nilai input {name} tidak valid.")

            if not (
                variable["universe"][0]
                <= value
                <= variable["universe"][-1]
            ):
                raise ValueError(f"Input {name} di luar domain.")

            fuzzified[name] = {
                label: float(np.interp(
                    value,
                    variable["universe"],
                    membership
                ))
                for label, membership in variable["mf"].items()
            }

        # Evaluasi aturan dan implikasi Mamdani
        z = self.output["universe"]
        aggregated = np.zeros_like(z)

        for rule in self.rules:
            antecedents, consequent = rule

            alpha = min(
                fuzzified[var][label]
                for var, label in antecedents
            )

            output_mf = self.output["mf"][consequent]

            # Implikasi menggunakan operator MIN
            implied = np.minimum(alpha, output_mf)

            # Agregasi menggunakan operator MAX
            aggregated = np.maximum(aggregated, implied)

        # Defuzzifikasi centroid
        area = np.trapezoid(aggregated, z)

        if area == 0:
            raise ValueError(
                "Tidak ada aturan aktif. Periksa fungsi keanggotaan "
                "dan basis aturan."
            )

        crisp = np.trapezoid(z * aggregated, z) / area

        return crisp


# ==========================================================
# 3. MEMBUAT DOMAIN DAN FUNGSI KEANGGOTAAN
# ==========================================================

# Lama langganan: 0-24 bulan
x1 = np.linspace(0, 24, 241)

mf_lama_langganan = {
    "Baru": trapmf(x1, [0, 0, 3, 12]),
    "Lama": trapmf(x1, [6, 12, 24, 24])
}

# Frekuensi transaksi: 0-15 kali per bulan
x2 = np.linspace(0, 15, 151)

mf_frekuensi = {
    "Jarang": trapmf(x2, [0, 0, 2, 8]),
    "Sering": trapmf(x2, [5, 10, 15, 15])
}

# Besaran diskon: 0-30 persen
z = np.linspace(0, 30, 301)

mf_diskon = {
    "Kecil": trimf(z, [0, 5, 12]),
    "Sedang": trimf(z, [8, 15, 22]),
    "Besar": trimf(z, [18, 25, 30])
}


# ==========================================================
# 4. MEMBANGUN SISTEM FIS
# ==========================================================

fis = FuzzyInferenceSystem()

fis.add_input_variable(
    "lama_langganan", x1, mf_lama_langganan
)

fis.add_input_variable(
    "frekuensi_transaksi", x2, mf_frekuensi
)

fis.set_output_variable(
    "diskon", z, mf_diskon
)


# Basis aturan fuzzy
fis.add_rule((
    [("lama_langganan", "Baru"),
     ("frekuensi_transaksi", "Jarang")],
    "Kecil"
))

fis.add_rule((
    [("lama_langganan", "Baru"),
     ("frekuensi_transaksi", "Sering")],
    "Sedang"
))

fis.add_rule((
    [("lama_langganan", "Lama"),
     ("frekuensi_transaksi", "Jarang")],
    "Sedang"
))

fis.add_rule((
    [("lama_langganan", "Lama"),
     ("frekuensi_transaksi", "Sering")],
    "Besar"
))


# ==========================================================
# 5. PENGUJIAN TIGA KASUS
# ==========================================================

kasus = [
    {"lama_langganan": 3, "frekuensi_transaksi": 2},
    {"lama_langganan": 12, "frekuensi_transaksi": 6},
    {"lama_langganan": 24, "frekuensi_transaksi": 15}
]

hasil = []

for i, data in enumerate(kasus, start=1):
    diskon = fis.compute(data)

    hasil.append(diskon)

    print(f"Kasus {i}")
    print(f"  Lama langganan      : {data['lama_langganan']} bulan")
    print(f"  Frekuensi transaksi : {data['frekuensi_transaksi']} kali/bulan")
    print(f"  Rekomendasi diskon  : {diskon:.2f}%")
    print("-" * 40)


# ==========================================================
# 6. VISUALISASI FUNGSI KEANGGOTAAN OUTPUT
# ==========================================================

plt.figure(figsize=(10, 5))

for label, membership in mf_diskon.items():
    plt.plot(z, membership, label=label)

plt.title("Fungsi Keanggotaan Besaran Diskon")
plt.xlabel("Diskon (%)")
plt.ylabel("Derajat Keanggotaan")
plt.ylim(-0.05, 1.05)
plt.grid(True, linestyle=":")
plt.legend()
plt.tight_layout()
plt.show()
