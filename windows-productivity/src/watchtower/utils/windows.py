"""
Watchtower Windows - Windows-Specific Utilities
Platform-specific integrations for Windows.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


def is_windows() -> bool:
    """Check if running on Windows."""
    return sys.platform == "win32" or os.name == "nt"


def get_data_directory() -> Path:
    """Get the appropriate data directory for the platform."""
    if is_windows():
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path.home()

    return base / ".watchtower"


async def send_notification(
    title: str,
    message: str,
    app_id: str = "Watchtower",
    silent: bool = False,
) -> bool:
    """
    Send a Windows toast notification.
    Uses PowerShell's BurntToast module if available, falls back to basic notification.
    """
    if not is_windows():
        print(f"[Notification] {title}: {message}")
        return True

    # Try BurntToast first (richer notifications)
    burnt_toast_command = f"""
        $ErrorActionPreference = 'SilentlyContinue'
        if (Get-Module -ListAvailable -Name BurntToast) {{
            Import-Module BurntToast
            New-BurntToastNotification -Text "{title}", "{message}" -AppLogo $null
            exit 0
        }}
        exit 1
    """

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", burnt_toast_command],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return True
    except Exception:
        pass

    # Fallback to basic Windows notification
    fallback_command = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

        $template = @"
        <toast>
          <visual>
            <binding template="ToastText02">
              <text id="1">{title}</text>
              <text id="2">{message}</text>
            </binding>
          </visual>
        </toast>
"@

        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("{app_id}").Show($toast)
    '''

    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", fallback_command],
            capture_output=True,
            text=True,
        )
        return True
    except Exception:
        # Final fallback: console output
        print(f"[Notification] {title}: {message}")
        return False


async def create_scheduled_task(
    name: str,
    command: str,
    time: str,
    days: Optional[list[str]] = None,
) -> bool:
    """
    Create a Windows Task Scheduler task for automated briefings.

    Args:
        name: Task name
        command: Command to run
        time: Time in HH:MM format
        days: Days of week (MON, TUE, WED, THU, FRI, SAT, SUN)
    """
    if not is_windows():
        print("Scheduled tasks only supported on Windows")
        return False

    days_of_week = ",".join(days) if days else "MON,TUE,WED,THU,FRI,SAT,SUN"

    create_task_command = f'''
        $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c {command}"
        $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek {days_of_week} -At "{time}"
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
        Register-ScheduledTask -TaskName "{name}" -Action $action -Trigger $trigger -Settings $settings -Force
    '''

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", create_task_command],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to create scheduled task: {e}")
        return False


async def remove_scheduled_task(name: str) -> bool:
    """Remove a Windows Task Scheduler task."""
    if not is_windows():
        return False

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"Unregister-ScheduledTask -TaskName '{name}' -Confirm:$false",
            ],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


async def open_with_default_app(file_path: str) -> None:
    """Open a file with the default Windows application."""
    if is_windows():
        os.startfile(file_path)  # type: ignore
    elif sys.platform == "darwin":
        subprocess.run(["open", file_path])
    else:
        subprocess.run(["xdg-open", file_path])


async def get_system_uptime() -> float:
    """Get system uptime in seconds to help detect fresh starts vs. sleep resume."""
    if is_windows():
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime | Select-Object -ExpandProperty TotalSeconds",
                ],
                capture_output=True,
                text=True,
            )
            return float(result.stdout.strip())
        except Exception:
            return 0.0
    return 0.0


async def is_on_battery() -> bool:
    """Check if the system is on battery power."""
    if not is_windows():
        return False

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-WmiObject -Class Win32_Battery).BatteryStatus",
            ],
            capture_output=True,
            text=True,
        )
        # BatteryStatus 1 = Discharging (on battery)
        return result.stdout.strip() == "1"
    except Exception:
        return False


async def get_windows_theme() -> str:
    """Get the current Windows theme (light/dark)."""
    if not is_windows():
        return "light"

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-ItemPropertyValue -Path 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize' -Name AppsUseLightTheme",
            ],
            capture_output=True,
            text=True,
        )
        return "dark" if result.stdout.strip() == "0" else "light"
    except Exception:
        return "light"


async def copy_to_clipboard(text: str) -> bool:
    """Copy text to Windows clipboard."""
    if not is_windows():
        print(f"Clipboard: {text}")
        return True

    try:
        # Escape for PowerShell
        escaped = text.replace("'", "''")
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{escaped}'"],
            capture_output=True,
            text=True,
        )
        return True
    except Exception:
        return False


async def get_clipboard() -> str:
    """Get clipboard contents."""
    if not is_windows():
        return ""

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return ""


async def play_sound(sound_type: str = "notification") -> None:
    """Play a system sound for notifications."""
    if not is_windows():
        return

    sounds = {
        "success": "Asterisk",
        "warning": "Exclamation",
        "error": "Hand",
        "notification": "Notification.Default",
    }

    sound_name = sounds.get(sound_type, "Notification.Default")

    try:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"[System.Media.SystemSounds]::{sound_name}.Play()",
            ],
            capture_output=True,
            text=True,
        )
    except Exception:
        pass  # Silent fail for sound


async def is_admin() -> bool:
    """Check if running with administrator privileges."""
    if not is_windows():
        return os.getuid() == 0 if hasattr(os, "getuid") else False

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)",
            ],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip().lower() == "true"
    except Exception:
        return False
