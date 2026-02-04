@echo off
echo ========================================
echo بناء ملف EXE
echo Building EXE File
echo ========================================
echo.

echo تثبيت PyInstaller...
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo بناء ملف EXE...
echo Building EXE...
pyinstaller --onefile --windowed --name=AudioMonitor --clean --noconfirm audio_monitor.py

echo.
echo ========================================
echo تم البناء بنجاح!
echo Build Complete!
echo ========================================
echo.
echo الملف موجود في: dist\AudioMonitor.exe  
echo File location: dist\AudioMonitor.exe
echo.
pause
