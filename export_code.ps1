#!/usr/bin/env pwsh
# Code Export Tool for Bana-TTS Project
param(
    [string]$Action = ""
)

function Show-Menu {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  Code Export Tool for Bana-TTS Project" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This script will export all your code files to HTML or PDF."
    Write-Host ""
    Write-Host "Choose your option:" -ForegroundColor Yellow
    Write-Host "  1. Preview files (see what will be included)"
    Write-Host "  2. Export to HTML (recommended - no dependencies)"
    Write-Host "  3. Export to PDF (requires reportlab installation)"
    Write-Host "  4. Install PDF dependencies"
    Write-Host "  5. Exit"
    Write-Host ""
}

function Preview-Files {
    Write-Host "Previewing files that would be included..." -ForegroundColor Green
    python export_code_to_html.py --preview
}

function Export-HTML {
    Write-Host "Creating HTML export..." -ForegroundColor Green
    python export_code_to_html.py --output bana_tts_code.html
    
    if (Test-Path "bana_tts_code.html") {
        Write-Host ""
        Write-Host "Opening HTML file in default browser..." -ForegroundColor Green
        Start-Process "bana_tts_code.html"
    }
}

function Export-PDF {
    Write-Host "Creating PDF export..." -ForegroundColor Green
    python export_code_to_pdf.py --output bana_tts_code.pdf
    
    if (Test-Path "bana_tts_code.pdf") {
        Write-Host ""
        Write-Host "Opening PDF file..." -ForegroundColor Green
        Start-Process "bana_tts_code.pdf"
    }
}

function Install-Dependencies {
    Write-Host "Installing PDF dependencies..." -ForegroundColor Green
    pip install reportlab
    Write-Host ""
    Write-Host "Installation complete!" -ForegroundColor Green
}

# Main script logic
if ($Action -eq "") {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-5)"
} else {
    $choice = $Action
}

switch ($choice) {
    "1" { Preview-Files }
    "2" { Export-HTML }
    "3" { Export-PDF }
    "4" { Install-Dependencies }
    "5" { 
        Write-Host ""
        Write-Host "Goodbye!" -ForegroundColor Green
        return
    }
    default {
        Write-Host ""
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
