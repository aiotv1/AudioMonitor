@echo off
echo ========================================
echo تثبيت المكتبات المطلوبة
echo Installing Required Libraries
echo ========================================
echo.

pip install -r requirements.txt

echo.
echo ========================================
echo تم التثبيت بنجاح!
echo Installation Complete!
echo ========================================
echo.
echo يمكنك الآن تشغيل البرنامج باستخدام:
echo You can now run the program using:
echo python audio_monitor.py
echo.
echo أو إنشاء ملف EXE:
echo Or build EXE file:
echo python build_exe.py
echo.
pause
