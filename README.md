# Legacy Android & XDA Hardware Bench

A classic XDA / Fastboot & ADB Terminal User Interface (TUI) for inspecting, rescuing, and tinkering with legacy Android devices on Linux and Windows.

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

## Compatibility & Supported Devices

`Legacy-Android-Bench` is built on top of standard Linux `adb` and `fastboot` protocols, supporting devices from **Android 2.3 (Gingerbread)** through modern Android versions.

### Feature & Protocol Compatibility

| Feature | Required Mode | Android Support | Compatible Brands / Devices |
| :--- | :--- | :--- | :--- |
| **Device & Root Inspector (`getprop`)** | ADB (Normal / Safe Mode) | Android 2.3+ | All Android devices (Samsung, HTC, LG, Sony, Motorola, Nexus, Xiaomi, Huawei, etc.) |
| **APK Installer & Live `logcat`** | ADB (Normal / Safe Mode) | Android 2.3+ | All Android devices with USB Debugging enabled |
| **Bloatware Freezer (`pm disable-user`)** | ADB (No Root Needed) | Android 5.0+ | All Android 5.0+ devices (older Android 4.x requires root) |
| **Recovery Sideload (`adb sideload`)** | Custom / Stock Recovery | Android 4.1+ | Devices running TWRP, ClockworkMod (CWM), Lineage Recovery, or stock sideload recovery |
| **Fastboot Info & `.img` Flasher** | Bootloader / Fastboot | All Versions | Google Nexus / Pixel, Motorola, HTC, Sony Xperia, OnePlus, Xiaomi, Asus |
| **Download Mode Reboot** | ADB | All Versions | Samsung Galaxy series (reboots into Odin / Heimdall mode) |

### Classic Legacy Devices Supported by These Protocols
- **Google / Nexus:** Galaxy Nexus (`maguro`), Nexus 4 (`mako`), Nexus 5 (`hammerhead`), Nexus 7 (`grouper` / `flo`)
- **Samsung Galaxy (ADB & Download Mode):** Galaxy S2 (`i9100`), Galaxy S3 (`i9300`), Galaxy S4 (`jfltexx`), Galaxy S5 (`klte`), Galaxy Note 2/3/4 *(Note: Samsung uses Odin/Heimdall instead of Fastboot for `.img` flashing)*
- **HTC (ADB & Fastboot):** HTC Desire, HTC One M7 (`m7`), HTC One M8 (`m8`), HTC HD2 (Android ports)
- **Motorola (ADB & Fastboot):** Moto G 1st/2nd Gen (`falcon` / `titan`), Moto X (`ghost`), Droid RAZR
- **Sony Xperia (ADB & Fastboot):** Xperia Z / Z1 / Z2 / Z3 series (with unlockable bootloaders)
- **LG (ADB):** LG G2 (`d802`), LG G3 (`d855`), Optimus series

> **Community Tested List:** Have you used `Legacy-Android-Bench` on a classic device? Open an Issue or Pull Request with your device model, codename, and Android version to add it here!

