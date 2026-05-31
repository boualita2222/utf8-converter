@echo off
title Convertisseur Unicode Complet - Python 3.14.2
color 0A

echo ======================================================
echo        CONVERTISSEUR UNICODE COMPLET
echo   UTF-8 / UTF-16BE / UTF-16LE / UTF-32BE / UTF-32LE
echo ======================================================
echo.

cd /d "C:\PythonProjets"

if exist "venv_314\Scripts\activate.bat" (
    call "venv_314\Scripts\activate.bat"
    python convertisseur_unicode_complet.py
) else (
    echo ERREUR: Environnement virtuel non trouve
    echo.
    echo Activez-le manuellement:
    echo .\venv_314\Scripts\Activate.ps1
    pause
    exit /b 1
)

pause
