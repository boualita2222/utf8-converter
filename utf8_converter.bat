@echo off
title Convertisseur UTF-8 - Python 3.14.2
color 0A

echo ======================================================
echo        CONVERTISSEUR UTF-8 COMPLET (1-4 octets)       
echo           Version Windows - Python 3.14.2             
echo ======================================================
echo.

REM Se placer dans le bon dossier
cd /d "C:\PythonProjets"

REM V?rifier si l'environnement virtuel existe
if exist "venv_314\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call "venv_314\Scripts\activate.bat"
) else (
    echo ERREUR: Environnement virtuel venv_314 non trouv?.
    echo.
    echo Activez-le manuellement avec:
    echo .\venv_314\Scripts\Activate.ps1
    echo.
    pause
    exit /b 1
)

REM V?rifier si le script Python existe
if exist "convertisseur_utf8.py" (
    echo Lancement du convertisseur UTF-8...
    echo ======================================================
    echo.
    python convertisseur_utf8.py
) else (
    echo ERREUR: Fichier convertisseur_utf8.py introuvable.
    echo.
    pause
)

REM Pause ? la fin pour voir les messages
echo.
echo ======================================================
echo Programme termin?. Appuyez sur une touche pour fermer.
echo ======================================================
pause
