# Register Mapache Skills Watcher as a Windows background task

$repoRoot = (Get-Item -Path $PSScriptRoot).Parent.FullName
$pythonPath = (Get-Command python).Source
$watcherPath = Join-Path $repoRoot "scripts\watch_skills.py"
$taskName = "MapacheSkillsWatcher"

# Ensure watchdog is installed
Write-Host "📦 Ensuring 'watchdog' is installed..." -ForegroundColor Cyan
& $pythonPath -m pip install watchdog --quiet

# Create the task
Write-Host "⚙️ Registering Windows Task: $taskName" -ForegroundColor Cyan

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $watcherPath -WorkingDirectory $repoRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Check if task already exists and remove it
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Write-Host "⚠️ Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName $taskName -Description "Monitors Mapache Skills directory for changes and auto-syncs to coding agents."

Write-Host "✅ Task registered successfully!" -ForegroundColor Green
Write-Host "🚀 Starting the watcher now..." -ForegroundColor Cyan
Start-ScheduledTask -TaskName $taskName

Write-Host "`n💡 The watcher is now running in the background. It will start automatically whenever you log in." -ForegroundColor White
