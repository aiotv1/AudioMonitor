# Audio Monitor
<img width="1640" height="664" alt="New Project (96)" src="https://github.com/user-attachments/assets/bd6aa237-b7ff-44df-9a20-3c2da84b5ce5" />
A system tray application that displays the icon of the currently playing audio application.

## 📋 Features

- ✅ Runs in the system tray next to the clock
- ✅ Monitors all applications producing audio
- ✅ Displays the icon of the active application producing sound
- ✅ Updates automatically when the application changes
- ✅ Simple and easy-to-use interface

## 🚀 Installation and Usage

### Method 1: Run the Program Directly (Requires Python)

1. **Install required libraries:**
```bash
pip install -r requirements.txt
```

2. **Run the program:**
```bash
python audio_monitor.py
```

### Method 2: Create an EXE File (Recommended)

1. **Install required libraries:**
```bash
pip install -r requirements.txt
pip install pyinstaller
```

2. **Create the EXE file:**
```bash
pyinstaller --onefile --windowed --name=AudioMonitor --clean audio_monitor.py
```

3. **Run the program:**
- Navigate to the `dist` folder
- Run `AudioMonitor.exe`
- The icon will appear in the system tray next to the clock

## 📖 How to Use

1. Run the program
2. An icon will appear in the system tray
3. When any audio plays (music, video, etc.), the icon will change to display the icon of the application producing the sound
4. Right-click on the icon to access the menu:
   - **About**: Display program information
   - **Exit**: Close the program

## 🛠️ Requirements

- Windows 10/11
- Python 3.7+ (if running the program directly)

## 📦 Libraries Used

- **pycaw**: For accessing Windows audio sessions
- **pystray**: For creating system tray icon
- **Pillow**: For image handling
- **psutil**: For process information
- **pywin32**: For accessing Windows API

## ⚠️ Notes

- The program works only on Windows
- Requires permissions to access audio and process information
- The icon updates every 0.5 seconds

## 📝 License

Free for personal and commercial use

---

Made with ❤️ for the community

