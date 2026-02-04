"""
Build script to create EXE file
سكريبت لإنشاء ملف exe
"""

import os
import subprocess
import sys

def build_exe():
    """بناء ملف exe باستخدام PyInstaller"""
    
    # التأكد من تثبيت PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("جاري تثبيت PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # معاملات PyInstaller
    pyinstaller_args = [
        'audio_monitor.py',
        '--onefile',                    # ملف واحد
        '--windowed',                   # بدون نافذة console
        '--name=AudioMonitor',          # اسم الملف
        '--icon=NONE',                  # يمكن إضافة أيقونة لاحقاً
        '--clean',                      # تنظيف الملفات المؤقتة
        '--noconfirm',                  # عدم طلب تأكيد
    ]
    
    print("جاري بناء ملف EXE...")
    print("هذا قد يستغرق بضع دقائق...")
    
    # تشغيل PyInstaller
    subprocess.check_call(['pyinstaller'] + pyinstaller_args)
    
    print("\n" + "="*50)
    print("✅ تم إنشاء الملف بنجاح!")
    print(f"📁 الملف موجود في: {os.path.join(os.getcwd(), 'dist', 'AudioMonitor.exe')}")
    print("="*50)

if __name__ == "__main__":
    build_exe()
