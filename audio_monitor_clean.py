"""
Audio Monitor - System Tray Application
يعرض أيقونة التطبيق الذي يصدر صوت في شريط المهام
"""

import time
import threading
import win32gui
import win32ui
import win32con
import win32api
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
import psutil
import comtypes


class AudioMonitor:
    def __init__(self):
        self.icon = None
        self.running = True
        self.current_app = None
        self.default_icon = self.create_default_icon()
        
    def create_default_icon(self):
        """إنشاء أيقونة افتراضية"""
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='#2c3e50')
        draw = ImageDraw.Draw(image)
        
        # رسم أيقونة سماعة بسيطة
        draw.ellipse([16, 16, 48, 48], fill='#3498db', outline='#ecf0f1', width=2)
        draw.rectangle([28, 32, 36, 52], fill='#ecf0f1')
        
        return image
    
    def get_process_icon(self, pid):
        """الحصول على أيقونة العملية من Process ID"""
        try:
            process = psutil.Process(pid)
            exe_path = process.exe()
            
            # استخراج الأيقونة من الملف التنفيذي
            ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
            ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
            
            large, small = win32gui.ExtractIconEx(exe_path, 0)
            
            if large:
                try:
                    win32gui.DestroyIcon(small[0])
                except:
                    pass
                    
                hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
                hdc = hdc.CreateCompatibleDC()
                
                hdc.SelectObject(hbmp)
                hdc.DrawIcon((0, 0), large[0])
                
                bmpinfo = hbmp.GetInfo()
                bmpstr = hbmp.GetBitmapBits(True)
                
                img = Image.frombuffer(
                    'RGBA',
                    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                    bmpstr, 'raw', 'BGRA', 0, 1
                )
                
                win32gui.DestroyIcon(large[0])
                
                # تغيير حجم الأيقونة
                img = img.resize((64, 64), Image.Resampling.LANCZOS)
                return img
            else:
                return self.default_icon
                
        except Exception as e:
            return self.default_icon
    
    def get_session_peak(self, session):
        """الحصول على قيمة Peak الفعلية من الجلسة"""
        try:
            meter = session._ctl.QueryInterface(IAudioMeterInformation)
            peak = meter.GetPeakValue()
            return peak
        except:
            return 0.0
    
    def get_active_audio_sessions(self):
        """الحصول على التطبيقات التي تصدر صوت حالياً"""
        try:
            sessions = AudioUtilities.GetAllSessions()
            active_apps = []
            
            for session in sessions:
                try:
                    if session.Process and session.Process.pid != 0:
                        # الحصول على Peak Value الحقيقي
                        peak = self.get_session_peak(session)
                        
                        volume = session.SimpleAudioVolume
                        is_muted = volume.GetMute() if volume else True
                        
                        # فقط إذا كان هناك صوت فعلي (peak > 0.001)
                        if peak > 0.001 and not is_muted:
                            active_apps.append({
                                'pid': session.Process.pid,
                                'name': session.Process.name(),
                                'peak': peak
                            })
                            
                except:
                    continue
            
            return active_apps
        except:
            return []
    
    def monitor_audio(self):
        """مراقبة الصوت بشكل مستمر"""
        comtypes.CoInitialize()
        
        try:
            while self.running:
                try:
                    active_apps = self.get_active_audio_sessions()
                    
                    if active_apps:
                        # اختيار التطبيق بأعلى peak
                        loudest_app = max(active_apps, key=lambda x: x['peak'])
                        
                        if self.current_app != loudest_app['pid']:
                            self.current_app = loudest_app['pid']
                            
                            # الحصول على أيقونة التطبيق
                            app_icon = self.get_process_icon(loudest_app['pid'])
                            
                            # تحديث أيقونة system tray
                            if self.icon:
                                self.icon.icon = app_icon
                                self.icon.title = f"🔊 {loudest_app['name']}"
                    else:
                        # لا يوجد صوت
                        if self.current_app is not None:
                            self.current_app = None
                            if self.icon:
                                self.icon.icon = self.default_icon
                                self.icon.title = "Audio Monitor - لا يوجد صوت"
                    
                    time.sleep(0.2)
                    
                except:
                    time.sleep(1)
        finally:
            comtypes.CoUninitialize()
    
    def quit_app(self, icon, item):
        """إغلاق البرنامج"""
        self.running = False
        icon.stop()
    
    def show_about(self, icon, item):
        """عرض معلومات عن البرنامج"""
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            "Audio Monitor v1.0\n\nيعرض أيقونة التطبيق الذي يصدر صوت",
            "حول البرنامج",
            0x40
        )
    
    def run(self):
        """تشغيل البرنامج"""
        # بدء مراقبة الصوت في خيط منفصل
        monitor_thread = threading.Thread(target=self.monitor_audio, daemon=True)
        monitor_thread.start()
        
        # إنشاء أيقونة system tray
        menu = pystray.Menu(
            item('حول البرنامج', self.show_about),
            item('إغلاق', self.quit_app)
        )
        
        self.icon = pystray.Icon(
            "audio_monitor",
            self.default_icon,
            "Audio Monitor - لا يوجد صوت",
            menu
        )
        
        # تشغيل الأيقونة
        self.icon.run()


if __name__ == "__main__":
    app = AudioMonitor()
    app.run()
