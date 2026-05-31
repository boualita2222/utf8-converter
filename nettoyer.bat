@'
@echo off
echo Nettoyage Python...

:: Cache Python
for /d /r "C:\PythonProjets" %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)

:: Fichiers .pyc
del /s /q "C:\PythonProjets\*.pyc" 2>nul

:: Cache pip
"C:\Program Files\Python314\python.exe" -m pip cache purge

:: Temp Windows
del /q /f /s "%TEMP%\*" 2>nul

echo OK - Nettoyage termine !
pause
'@ | Set-Content "$env:USERPROFILE\Desktop\nettoyer.bat" -Encoding UTF8
Write-Host "OK - Script cree sur le Bureau !"