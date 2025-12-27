/**
 * Watchtower Windows - Windows-Specific Utilities
 * Platform-specific integrations for Windows
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import { platform } from 'os';
import { join } from 'path';

const execAsync = promisify(exec);

/**
 * Check if running on Windows
 */
export function isWindows(): boolean {
  return platform() === 'win32';
}

/**
 * Get the appropriate data directory for the platform
 */
export function getDataDirectory(): string {
  if (isWindows()) {
    return process.env.APPDATA
      ? join(process.env.APPDATA, 'watchtower')
      : join(process.env.USERPROFILE || '', '.watchtower');
  }
  return join(process.env.HOME || '', '.watchtower');
}

/**
 * Send a Windows toast notification
 * Uses PowerShell's BurntToast module if available, falls back to basic notification
 */
export async function sendNotification(
  title: string,
  message: string,
  options: {
    silent?: boolean;
    appId?: string;
  } = {}
): Promise<boolean> {
  if (!isWindows()) {
    console.log(`[Notification] ${title}: ${message}`);
    return true;
  }

  const appId = options.appId || 'Watchtower';

  // Try BurntToast first (richer notifications)
  const burntToastCommand = `
    $ErrorActionPreference = 'SilentlyContinue'
    if (Get-Module -ListAvailable -Name BurntToast) {
      Import-Module BurntToast
      New-BurntToastNotification -Text "${title}", "${message}" -AppLogo $null
      exit 0
    }
    exit 1
  `;

  try {
    await execAsync(`powershell -NoProfile -Command "${burntToastCommand.replace(/\n/g, ' ')}"`);
    return true;
  } catch {
    // Fallback to basic Windows notification
    const fallbackCommand = `
      [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
      [Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
      [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

      $template = @"
      <toast>
        <visual>
          <binding template="ToastText02">
            <text id="1">${title}</text>
            <text id="2">${message}</text>
          </binding>
        </visual>
      </toast>
"@

      $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
      $xml.LoadXml($template)
      $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
      [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("${appId}").Show($toast)
    `;

    try {
      await execAsync(`powershell -NoProfile -Command "${fallbackCommand.replace(/\n/g, ' ')}"`);
      return true;
    } catch {
      // Final fallback: console output
      console.log(`[Notification] ${title}: ${message}`);
      return false;
    }
  }
}

/**
 * Create a Windows Task Scheduler task for automated briefings
 */
export async function createScheduledTask(
  name: string,
  command: string,
  schedule: {
    time: string; // HH:MM format
    days?: ('MON' | 'TUE' | 'WED' | 'THU' | 'FRI' | 'SAT' | 'SUN')[];
  }
): Promise<boolean> {
  if (!isWindows()) {
    console.log(`Scheduled tasks only supported on Windows`);
    return false;
  }

  const daysOfWeek = schedule.days?.join(',') || 'MON,TUE,WED,THU,FRI,SAT,SUN';

  const createTaskCommand = `
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c ${command}"
    $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek ${daysOfWeek} -At "${schedule.time}"
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    Register-ScheduledTask -TaskName "${name}" -Action $action -Trigger $trigger -Settings $settings -Force
  `;

  try {
    await execAsync(`powershell -NoProfile -Command "${createTaskCommand.replace(/\n/g, ' ')}"`);
    return true;
  } catch (error) {
    console.error(`Failed to create scheduled task: ${error}`);
    return false;
  }
}

/**
 * Remove a Windows Task Scheduler task
 */
export async function removeScheduledTask(name: string): Promise<boolean> {
  if (!isWindows()) {
    return false;
  }

  try {
    await execAsync(`powershell -NoProfile -Command "Unregister-ScheduledTask -TaskName '${name}' -Confirm:$false"`);
    return true;
  } catch {
    return false;
  }
}

/**
 * Open a file with the default Windows application
 */
export async function openWithDefaultApp(filePath: string): Promise<void> {
  if (isWindows()) {
    await execAsync(`start "" "${filePath}"`);
  } else if (platform() === 'darwin') {
    await execAsync(`open "${filePath}"`);
  } else {
    await execAsync(`xdg-open "${filePath}"`);
  }
}

/**
 * Get system uptime to help detect fresh starts vs. sleep resume
 */
export async function getSystemUptime(): Promise<number> {
  if (isWindows()) {
    try {
      const { stdout } = await execAsync(
        'powershell -NoProfile -Command "(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime | Select-Object -ExpandProperty TotalSeconds"'
      );
      return parseFloat(stdout.trim());
    } catch {
      return 0;
    }
  }
  return process.uptime();
}

/**
 * Check if the system is on battery power
 */
export async function isOnBattery(): Promise<boolean> {
  if (!isWindows()) {
    return false;
  }

  try {
    const { stdout } = await execAsync(
      'powershell -NoProfile -Command "(Get-WmiObject -Class Win32_Battery).BatteryStatus"'
    );
    // BatteryStatus 1 = Discharging (on battery)
    return stdout.trim() === '1';
  } catch {
    return false;
  }
}

/**
 * Get the current Windows theme (light/dark)
 */
export async function getWindowsTheme(): Promise<'light' | 'dark'> {
  if (!isWindows()) {
    return 'light';
  }

  try {
    const { stdout } = await execAsync(
      'powershell -NoProfile -Command "Get-ItemPropertyValue -Path \'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize\' -Name AppsUseLightTheme"'
    );
    return stdout.trim() === '0' ? 'dark' : 'light';
  } catch {
    return 'light';
  }
}

/**
 * Copy text to Windows clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  if (!isWindows()) {
    console.log(`Clipboard: ${text}`);
    return true;
  }

  try {
    // Escape for PowerShell
    const escaped = text.replace(/'/g, "''");
    await execAsync(`powershell -NoProfile -Command "Set-Clipboard -Value '${escaped}'"`);
    return true;
  } catch {
    return false;
  }
}

/**
 * Get clipboard contents
 */
export async function getClipboard(): Promise<string> {
  if (!isWindows()) {
    return '';
  }

  try {
    const { stdout } = await execAsync('powershell -NoProfile -Command "Get-Clipboard"');
    return stdout.trim();
  } catch {
    return '';
  }
}

/**
 * Play a system sound for notifications
 */
export async function playSound(soundType: 'success' | 'warning' | 'error' | 'notification'): Promise<void> {
  if (!isWindows()) {
    return;
  }

  const sounds: Record<string, string> = {
    success: 'Asterisk',
    warning: 'Exclamation',
    error: 'Hand',
    notification: 'Notification.Default',
  };

  try {
    await execAsync(
      `powershell -NoProfile -Command "[System.Media.SystemSounds]::${sounds[soundType]}.Play()"`
    );
  } catch {
    // Silent fail for sound
  }
}

/**
 * Check if running with administrator privileges
 */
export async function isAdmin(): Promise<boolean> {
  if (!isWindows()) {
    return process.getuid?.() === 0;
  }

  try {
    const { stdout } = await execAsync(
      'powershell -NoProfile -Command "([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"'
    );
    return stdout.trim().toLowerCase() === 'true';
  } catch {
    return false;
  }
}
