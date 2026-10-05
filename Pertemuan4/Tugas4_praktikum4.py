# ==========================================================
# KASUS: EVALUASI KELAYAKAN BANDWIDTH JARINGAN KAMPUS
# ==========================================================

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate

# ----------------------------------------------------------
# 1. DEFINISI FUNGSI KEANGGOTAAN (MEMBERSHIP FUNCTIONS)
# ----------------------------------------------------------
def tri_mf(x, a, b, c):
  """Fungsi Keanggotaan Segitiga"""
  return np.maximum(0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))

def trap_mf(x, a, b, c, d):
  """Fungsi Keanggotaan Trapesium"""
  return np.maximum(
      0, np.minimum(np.minimum((x - a) / (b - a), 1), (d - x) / (d - c))
  )

# ----------------------------------------------------------
# 2. PENGUJIAN PADA 4 TITIK THROUGHPUT
# ----------------------------------------------------------
x_test = np.array([35, 50, 65, 80])

# Derajat Keanggotaan Dasar
muA = tri_mf(x_test, 30, 60, 90)  # Himpunan A: Segitiga [30, 60, 90]
muB = trap_mf(x_test, 40, 55, 75, 95)  # Himpunan B: Trapesium [40, 55, 75, 95]

# Operasi Logika Fuzzy
comp_A = 1 - muA
z_min = np.minimum(muA, muB)
a_prod = muA * muB
z_max = np.maximum(muA, muB)
a_sum = muA + muB - (muA * muB)

# Buat DataFrame untuk Output Terminal Bergaris (Grid)
df = pd.DataFrame({
    'Throughput (Mbps)': x_test,
    'mu_A (Bandwidth)': [f'{v:.4f}' for v in muA],
    'mu_B (Packet Loss)': [f'{v:.4f}' for v in muB],
    '¬A (Komplemen)': [f'{v:.4f}' for v in comp_A],
    'Zadeh Min': [f'{v:.4f}' for v in z_min],
    'Alg Product': [f'{v:.4f}' for v in a_prod],
    'Zadeh Max': [f'{v:.4f}' for v in z_max],
    'Alg Sum': [f'{v:.4f}' for v in a_sum],
})

tabel_terminal = tabulate(df, headers='keys', tablefmt='grid', showindex=False)

print('=' * 105)
print('KASUS: EVALUASI KELAYAKAN BANDWIDTH JARINGAN KAMPUS'.center(105))
print('=' * 105)
print(tabel_terminal)
print('=' * 105)

# ----------------------------------------------------------
# 3. PLOTTING GRAFIK VISUALISASI
# ----------------------------------------------------------
x_full = np.linspace(0, 100, 1001)

muA_full = tri_mf(x_full, 30, 60, 90)
muB_full = trap_mf(x_full, 40, 55, 75, 95)

z_min_full = np.minimum(muA_full, muB_full)
a_prod_full = muA_full * muB_full
z_max_full = np.maximum(muA_full, muB_full)
a_sum_full = muA_full + muB_full - (muA_full * muB_full)
comp_A_full = 1 - muA_full

fig, axes = plt.subplots(3, 1, figsize=(11, 13), sharex=True)

# Panel 1: Fungsi Keanggotaan Dasar A, B, dan Komplemen ¬A
axes[0].plot(
    x_full,
    muA_full,
    'b-',
    label='Himpunan A (Bandwidth - Segitiga [30,60,90])',
    linewidth=2,
)
axes[0].plot(
    x_full,
    muB_full,
    'g-',
    label='Himpunan B (Loss - Trapesium [40,55,75,95])',
    linewidth=2,
)
axes[0].plot(
    x_full,
    comp_A_full,
    'r--',
    label='Komplemen ¬A (1 - μA)',
    linewidth=1.5,
)
axes[0].set_title(
    '1. Fungsi Keanggotaan Dasar A, B, dan Komplemen ¬A',
    fontsize=12,
    pad=10,
    fontweight='bold',
)
axes[0].set_ylabel('Derajat Keanggotaan (μ)', fontsize=10)
axes[0].grid(True, linestyle=':', alpha=0.6)
axes[0].legend(loc='upper right')

# Panel 2: Operasi Irisan
axes[1].plot(x_full, muA_full, 'b:', alpha=0.35, label='μA')
axes[1].plot(x_full, muB_full, 'g:', alpha=0.35, label='μB')
axes[1].plot(
    x_full,
    z_min_full,
    'm-',
    label='Irisan: Zadeh Min (min(μA, μB))',
    linewidth=2,
)
axes[1].plot(
    x_full,
    a_prod_full,
    'c--',
    label='Irisan: Algebraic Product (μA × μB)',
    linewidth=2,
)
axes[1].set_title(
    '2. Operasi Irisan (Intersection)',
    fontsize=12,
    pad=10,
    fontweight='bold',
)
axes[1].set_ylabel('Derajat Keanggotaan (μ)', fontsize=10)
axes[1].grid(True, linestyle=':', alpha=0.6)
axes[1].legend(loc='upper right')

# Panel 3: Operasi Gabungan
axes[2].plot(x_full, muA_full, 'b:', alpha=0.35, label='μA')
axes[2].plot(x_full, muB_full, 'g:', alpha=0.35, label='μB')
axes[2].plot(
    x_full,
    z_max_full,
    color='orange',
    label='Gabungan: Zadeh Max (max(μA, μB))',
    linewidth=2,
)
axes[2].plot(
    x_full,
    a_sum_full,
    color='purple',
    linestyle='--',
    label='Gabungan: Algebraic Sum (μA + μB - μA×μB)',
    linewidth=2,
)
axes[2].set_title(
    '3. Operasi Gabungan (Union)', fontsize=12, pad=10, fontweight='bold'
)
axes[2].set_xlabel('Throughput Efektif (Mbps)', fontsize=10)
axes[2].set_ylabel('Derajat Keanggotaan (μ)', fontsize=10)
axes[2].grid(True, linestyle=':', alpha=0.6)
axes[2].legend(loc='upper right')

plt.tight_layout()
plt.savefig('grafik_evaluasi_bandwidth_lengkap_v2.png', dpi=300)
plt.show()
