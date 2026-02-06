# Add Git to System PATH permanently
$gitPath = "C:\Program Files\Git\bin"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath -notlike "*$gitPath*") {
    $newPath = $currentPath + ";$gitPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Git path added to system environment!" -ForegroundColor Green
    Write-Host "Please close and reopen PowerShell/CMD for changes to take effect."
} else {
    Write-Host "Git path is already in system environment." -ForegroundColor Yellow
}

# Test git command
& "C:\Program Files\Git\bin\git.exe" --version
