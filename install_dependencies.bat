@echo off
echo Installing required packages for code export tool...
pip install reportlab
echo.
echo Installation complete! You can now run the code export tool.
echo.
echo Usage examples:
echo   python export_code_to_pdf.py --preview
echo   python export_code_to_pdf.py --output my_code.pdf
echo.
pause
