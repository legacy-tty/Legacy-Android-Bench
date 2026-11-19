# Legacy Android & XDA Hardware Bench

A classic XDA / Fastboot & ADB Terminal User Interface (TUI) for inspecting, rescuing, and tinkering with legacy Android devices on Linux.

## Features
- **ADB & Fastboot Inspector:** Reads device codename, Android version, API level, build ID, root (`su`) status, bootloader state, and battery level.
- **Hardware Reboot Menu:** One-click reboot into Normal, Recovery (TWRP/CWM), Bootloader/Fastboot, or Samsung Download Mode.
- **APK & Package Manager:** Batch install `.apk` files or disable pre-installed system bloatware without root.
- **Flashing & Sideload Helper:** Safely flash recovery `.img` files via Fastboot or sideload `.zip` ROMs via ADB.
- **Live Error Logcat:** Streams filtered fatal errors and crashes (`*:E`) in real time.

## Quick Start (Linux Mint / Ubuntu / Debian)

1. Install system dependencies:
   ```bash
   sudo apt update && sudo apt install git android-tools-adb android-tools-fastboot python3-venv -y
   ```

2. Clone and run with the automatic launcher:
   ```bash
   git clone https://github.com/legacy-tty/Legacy-Android-Bench
   cd Legacy-Android-Bench
   bash run.sh
   ```


   SCRENSHOOTS:
   <img width="641" height="411" alt="Screenshot_2026-11-19_20-18-49" src="https://github.com/user-attachments/assets/aa5241e7-dead-4ecc-b62e-dcde001e8441" />

