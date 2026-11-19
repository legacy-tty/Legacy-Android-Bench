#!/usr/bin/env python3
import os
import shutil
import subprocess
import time

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

BANNER = r"""
  _      ______ _____          _______     __           _____  ____   ____ _______ 
 | |    |  ____/ ____|   /\   / ____\ \   / /     /\   |  __ \|  _ \ / __ \__   __|
 | |    | |__ | |  __   /  \ | |     \ \_/ /     /  \  | |  | | |_) | |  | | | |   
 | |    |  __|| | |_ | / /\ \| |      \   /     / /\ \ | |  | |  _ <| |  | | | |   
 | |____| |___| |__| |/ ____ \ |____   | |     / ____ \| |__| | |_) | |__| | | |   
 |______|______\_____/_/    \_\_____|  |_|    /_/    \_\_____/|____/ \____/  |_|   
"""


def run_cmd(cmd, timeout=10):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out."
    except FileNotFoundError:
        return -1, "", f"Tool not found: {cmd}"


def draw_header():
    console.clear()
    banner_txt = Text(BANNER, style="bold green")
    sub_txt = Text(
        "  [ XDA / Fastboot & ADB Hardware Bench v1.0 | Legacy Android Edition ]",
        style="bold cyan",
    )
    console.print(
        Panel(
            Text.assemble(banner_txt, "\n", sub_txt),
            border_style="bright_green",
            padding=(0, 1),
        )
    )


def pause():
    console.print("\n[dim]Press Enter to return to Main Menu...[/dim]")
    input()


def check_tools():
    missing = []
    if not shutil.which("adb"):
        missing.append("adb")
    if not shutil.which("fastboot"):
        missing.append("fastboot")
    if missing:
        console.print(
            Panel(
                f"[bold red]Missing system tools: {', '.join(missing)}[/bold red]\n"
                "Install them on Linux Mint with:\n"
                "[cyan]sudo apt install android-tools-adb android-tools-fastboot[/cyan]",
                border_style="red",
            )
        )
        return False
    return True


def get_adb_devices():
    code, out, _ = run_cmd(["adb", "devices"])
    devices = []
    if code == 0:
        for line in out.splitlines()[1:]:
            if "\tdevice" in line:
                devices.append(line.split("\t")[0])
    return devices


def get_fastboot_devices():
    code, out, _ = run_cmd(["fastboot", "devices"])
    devices = []
    if code == 0:
        for line in out.splitlines():
            if "\tfastboot" in line:
                devices.append(line.split("\t")[0])
    return devices


def inspect_android():
    draw_header()
    if not check_tools():
        pause()
        return

    console.print("[bold yellow]>>> Scanning ADB & Fastboot Interfaces...[/bold yellow]\n")
    adb_devs = get_adb_devices()
    fb_devs = get_fastboot_devices()

    if adb_devs:
        serial = adb_devs[0]
        props = {
            "Manufacturer": "ro.product.manufacturer",
            "Model": "ro.product.model",
            "Device Codename": "ro.product.device",
            "Android Version": "ro.build.version.release",
            "SDK / API Level": "ro.build.version.sdk",
            "Build ID": "ro.build.display.id",
            "CPU Architecture": "ro.product.cpu.abi",
            "Kernel / Baseband": "gsm.version.baseband",
            "Bootloader Version": "ro.bootloader",
        }

        table = Table(title=f"ADB Device Connected [{serial}]", border_style="green")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="bold white")

        for label, prop in props.items():
            _, val, _ = run_cmd(["adb", "-s", serial, "shell", "getprop", prop])
            table.add_row(label, val if val else "[dim]N/A[/dim]")

        _, su_out, _ = run_cmd(["adb", "-s", serial, "shell", "which su"])
        root_status = "[bold green]ROOTED (su found)[/bold green]" if su_out else "[yellow]Unrooted (Stock)[/yellow]"
        table.add_row("Root Access", root_status)

        _, bat_out, _ = run_cmd(["adb", "-s", serial, "shell", "dumpsys battery"])
        for line in bat_out.splitlines():
            if "level:" in line:
                table.add_row("Battery Level", f"{line.split(':')[1].strip()}%")
                break

        console.print(table)

    elif fb_devs:
        serial = fb_devs[0]
        table = Table(title=f"Fastboot / Bootloader Device [{serial}]", border_style="yellow")
        table.add_column("Fastboot Variable", style="cyan")
        table.add_column("Value", style="bold white")

        for var in ["product", "variant", "version-bootloader", "version-baseband", "unlocked", "secure"]:
            _, _, err = run_cmd(["fastboot", "-s", serial, "getvar", var])
            val = ""
            for line in err.splitlines():
                if line.startswith(f"{var}:"):
                    val = line.split(":", 1)[1].strip()
            table.add_row(var, val if val else "[dim]N/A[/dim]")

        console.print(table)
    else:
        console.print(
            Panel(
                "[yellow]No Android devices detected in ADB or Fastboot mode.[/yellow]\n\n"
                "[white]Troubleshooting Checklist for Legacy Android:[/white]\n"
                "1. Enable [bold]USB Debugging[/bold] in Settings -> Developer Options.\n"
                "2. Switch USB mode from 'Charge Only' to [bold]MTP / File Transfer[/bold].\n"
                "3. Accept the [bold]'Allow USB Debugging'[/bold] RSA fingerprint pop-up on the phone.",
                border_style="yellow",
            )
        )

    pause()


def reboot_menu():
    draw_header()
    if not check_tools():
        pause()
        return

    adb_devs = get_adb_devices()
    fb_devs = get_fastboot_devices()

    if not adb_devs and not fb_devs:
        console.print("[bold red]No device connected via ADB or Fastboot![/bold red]")
        pause()
        return

    target = questionary.select(
        "Select Target Boot Mode:",
        choices=[
            "1. Normal System Reboot",
            "2. Reboot to Recovery (TWRP / CWM / Stock Recovery)",
            "3. Reboot to Bootloader / Fastboot Mode",
            "4. Reboot to Download Mode (Samsung Odin)",
            "5. Back to Main Menu",
        ],
    ).ask()

    if not target or target.startswith("5."):
        return

    if adb_devs:
        serial = adb_devs[0]
        if target.startswith("1."):
            run_cmd(["adb", "-s", serial, "reboot"])
        elif target.startswith("2."):
            run_cmd(["adb", "-s", serial, "reboot", "recovery"])
        elif target.startswith("3."):
            run_cmd(["adb", "-s", serial, "reboot", "bootloader"])
        elif target.startswith("4."):
            run_cmd(["adb", "-s", serial, "reboot", "download"])
        console.print("[bold green]✔ Reboot command sent via ADB![/bold green]")
    elif fb_devs:
        serial = fb_devs[0]
        if target.startswith("1."):
            run_cmd(["fastboot", "-s", serial, "reboot"])
        elif target.startswith("3."):
            run_cmd(["fastboot", "-s", serial, "reboot-bootloader"])
        else:
            console.print("[yellow]Fastboot only supports Normal or Bootloader reboot directly.[/yellow]")
            pause()
            return
        console.print("[bold green]✔ Reboot command sent via Fastboot![/bold green]")

    pause()


def apk_and_packages():
    draw_header()
    if not check_tools():
        pause()
        return

    adb_devs = get_adb_devices()
    if not adb_devs:
        console.print("[bold red]Connect an Android device in ADB mode first![/bold red]")
        pause()
        return

    serial = adb_devs[0]
    action = questionary.select(
        "APK & Package Manager:",
        choices=[
            "1. Install an .APK file onto device",
            "2. List all installed third-party packages",
            "3. Disable / Freeze a bloatware package (No Root Needed)",
            "4. Back to Main Menu",
        ],
    ).ask()

    if not action or action.startswith("4."):
        return

    if action.startswith("1."):
        apk_path = questionary.path("Select .apk file to install:").ask()
        if apk_path:
            apk_path = os.path.expanduser(apk_path.strip())
            console.print(f"\n[cyan]Installing {os.path.basename(apk_path)}...[/cyan]")
            code, out, err = run_cmd(["adb", "-s", serial, "install", "-r", apk_path], timeout=60)
            if code == 0 and "Success" in out:
                console.print("[bold green]✔ APK Installed Successfully![/bold green]")
            else:
                console.print(f"[bold red]✘ Failed:[/bold red] {out} {err}")

    elif action.startswith("2."):
        console.print("\n[cyan]Fetching installed user packages...[/cyan]\n")
        _, out, _ = run_cmd(["adb", "-s", serial, "shell", "pm", "list", "packages", "-3"])
        pkgs = [line.replace("package:", "") for line in out.splitlines()]
        if pkgs:
            for p in sorted(pkgs):
                console.print(f"  [green]•[/green] {p}")
            console.print(f"\n[dim]Total user apps: {len(pkgs)}[/dim]")
        else:
            console.print("[yellow]No third-party packages found.[/yellow]")

    elif action.startswith("3."):
        pkg = questionary.text("Enter exact package name to disable (e.g., com.facebook.katana):").ask()
        if pkg and pkg.strip():
            code, out, err = run_cmd(
                ["adb", "-s", serial, "shell", "pm", "disable-user", "--user", "0", pkg.strip()]
            )
            if "disabled" in out.lower():
                console.print(f"[bold green]✔ Disabled {pkg.strip()}![/bold green]")
            else:
                console.print(f"[bold red]✘ Error:[/bold red] {out} {err}")

    pause()


def flash_sideload_helper():
    draw_header()
    if not check_tools():
        pause()
        return

    mode = questionary.select(
        "Flashing & Sideload Utility:",
        choices=[
            "1. ADB Sideload a ROM / GApps .zip (Device must be in Recovery Sideload mode)",
            "2. Fastboot Flash Recovery .img (TWRP / CWM - Device must be in Fastboot mode)",
            "3. Back to Main Menu",
        ],
    ).ask()

    if not mode or mode.startswith("3."):
        return

    if mode.startswith("1."):
        zip_path = questionary.path("Select .zip file to sideload:").ask()
        if not zip_path:
            return
        zip_path = os.path.expanduser(zip_path.strip())
        if not os.path.isfile(zip_path):
            console.print("[bold red]File not found![/bold red]")
            pause()
            return

        if questionary.confirm(f"Start ADB sideload for {os.path.basename(zip_path)}?").ask():
            console.print("\n[bold yellow]>>> Sideloading... Do not unplug USB cable![/bold yellow]\n")
            subprocess.run(["adb", "sideload", zip_path])

    elif mode.startswith("2."):
        fb_devs = get_fastboot_devices()
        if not fb_devs:
            console.print("[bold red]No device detected in Fastboot mode![/bold red]")
            pause()
            return

        img_path = questionary.path("Select recovery .img file:").ask()
        if not img_path:
            return
        img_path = os.path.expanduser(img_path.strip())
        if not os.path.isfile(img_path):
            console.print("[bold red]File not found![/bold red]")
            pause()
            return

        console.print(
            Panel(
                f"[bold red]WARNING:[/bold red] Flashing [cyan]{os.path.basename(img_path)}[/cyan] to [bold]recovery[/bold] partition.\n"
                "Make sure this image matches your exact device codename!",
                border_style="red",
            )
        )
        if questionary.confirm("Proceed with fastboot flash recovery?").ask():
            subprocess.run(["fastboot", "flash", "recovery", img_path])

    pause()


def live_logcat():
    draw_header()
    if not check_tools():
        pause()
        return

    adb_devs = get_adb_devices()
    if not adb_devs:
        console.print("[bold red]Connect an Android device in ADB mode first![/bold red]")
        pause()
        return

    console.print("[bold yellow]>>> Streaming Android Error Logcat (*:E) — Press Ctrl+C to Stop[/bold yellow]\n")
    time.sleep(1)
    try:
        subprocess.run(["adb", "logcat", "*:E"])
    except KeyboardInterrupt:
        console.print("\n[cyan]Logcat stream stopped.[/cyan]")
    pause()


def main():
    while True:
        draw_header()
        choice = questionary.select(
            "Select Android Operation:",
            choices=[
                "1. Inspect Device Info, Root Status & Bootloader (ADB / Fastboot)",
                "2. Hardware Reboot Menu (Recovery / Bootloader / Download Mode)",
                "3. APK Installer & Bloatware Freezer",
                "4. Flash Recovery (.img) or ADB Sideload ROM (.zip)",
                "5. Stream Live Crash & Error Logcat",
                "6. Exit Bench",
            ],
            qmark="[*]",
            pointer=">>",
        ).ask()

        if choice is None or choice.startswith("6."):
            console.print("\n[bold green]Exiting Legacy Android Bench. Happy flashing![/bold green]")
            break
        elif choice.startswith("1."):
            inspect_android()
        elif choice.startswith("2."):
            reboot_menu()
        elif choice.startswith("3."):
            apk_and_packages()
        elif choice.startswith("4."):
            flash_sideload_helper()
        elif choice.startswith("5."):
            live_logcat()


if __name__ == "__main__":
    main()
