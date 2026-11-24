@echo off
title SmartRetail - Web App Streamlit
cd /d "%~dp0"
echo ============================================================
echo Menjalankan Web App Fuzzy SmartRetail-Diskon dengan Streamlit...
echo ============================================================
echo.
python -m streamlit run "Modul3_240306013_Hilmifarelarrazak.ipynb\src\app.py"
pause
