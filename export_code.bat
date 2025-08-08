@echo off
echo ==========================================
echo   Code Export Tool for Bana-TTS Project
echo ==========================================
echo.
echo This script will export all your code files to HTML or PDF.
echo.
echo Choose your option:
echo   1. Preview files (see what will be included)
echo   2. Export to HTML (recommended - no dependencies)
echo   3. Export to PDF (requires reportlab installation)
echo   4. Install PDF dependencies
echo   5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Previewing files that would be included...
    python export_code_to_html.py --preview
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Creating HTML export...
    python export_code_to_html.py --output bana_tts_code.html
    echo.
    echo Opening HTML file in default browser...
    start bana_tts_code.html
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Creating PDF export...
    python export_code_to_pdf.py --output bana_tts_code.pdf
    if exist bana_tts_code.pdf (
        echo.
        echo Opening PDF file...
        start bana_tts_code.pdf
    )
    goto end
)

if "%choice%"=="4" (
    echo.
    echo Installing PDF dependencies...
    call install_dependencies.bat
    goto end
)

if "%choice%"=="5" (
    echo.
    echo Goodbye!
    goto end
)

echo.
echo Invalid choice. Please run the script again.

:end
echo.
pause
