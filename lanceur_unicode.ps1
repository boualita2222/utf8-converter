# lanceur_unicode.ps1
$host.UI.RawUI.WindowTitle = "Convertisseur Unicode Complet"

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location "C:\PythonProjets"

Write-Host "=== CONVERTISSEUR UNICODE COMPLET ===" -ForegroundColor Cyan
Write-Host "UTF-8 / UTF-16BE / UTF-16LE / UTF-32BE / UTF-32LE" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "venv_314\Scripts\Activate.ps1") {
    & ".\venv_314\Scripts\Activate.ps1"
    python .\convertisseur_unicode_complet.py
} else {
    Write-Host "ERREUR: Environnement virtuel non trouve" -ForegroundColor Red
    Write-Host "Activez-le avec: .\venv_314\Scripts\Activate.ps1" -ForegroundColor Yellow
}

Read-Host "`nAppuyez sur Entree pour quitter"
