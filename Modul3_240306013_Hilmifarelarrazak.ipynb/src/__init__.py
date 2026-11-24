"""
Paket Modul Sistem Pendukung Keputusan Fuzzy untuk Diskon Toko
SmartRetail-Diskon Engine
"""
from .fuzzy_engine import (
    DiskonTokoFuzzyEngine,
    trapezoid,
    triangle,
    RULES
)

__all__ = [
    "DiskonTokoFuzzyEngine",
    "trapezoid",
    "triangle",
    "RULES"
]
