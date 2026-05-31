# lanceur.ps1 - Lanceur PowerShell pour le Convertisseur UTF-8
$host.UI.RawUI.WindowTitle = "Convertisseur UTF-8 - PowerShell"

# Aller au dossier du projet
Set-Location "C:\PythonProjets"

# Activer l'environnement virtuel
if (Test-Path "venv_314\Scripts\Activate.ps1") {
    & ".\venv_314\Scripts\Activate.ps1"
    Write-Host "Convertisseur UTF-8 - Python 3.14.2" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    python .\convertisseur_utf8.py
} else {
    Write-Host "ERREUR: Environnement virtuel 'venv_314' non trouvé!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Pour créer l'environnement, exécutez:" -ForegroundColor Yellow
    Write-Host "1. cd C:\PythonProjets" -ForegroundColor White
    Write-Host "2. python -m venv venv_314" -ForegroundColor White
    Write-Host "3. .\venv_314\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "4. pip install colorama" -ForegroundColor White
}

Read-Host "`nAppuyez sur Entrée pour quitter"
