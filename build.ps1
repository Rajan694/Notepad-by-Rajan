param(
    [ValidateSet("windows", "linux", IgnoreCase = $true)]
    [string]$Target = "windows"
)

$ErrorActionPreference = "Stop"

$Target = $Target.ToLower()
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "=== Building Notepad for target: $Target ===" -ForegroundColor Cyan

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found. Installing via pip..." -ForegroundColor Yellow
    pip install pyinstaller
}

$IconFlag = ""
if (Test-Path "note.ico") {
    if ($Target -eq "windows") {
        $IconFlag = '--icon=note.ico --add-data "note.ico;."'
    } else {
        $IconFlag = '--icon=note.ico --add-data "note.ico:."'
    }
}

switch ($Target) {
    "windows" {
        Write-Host "Building Windows standalone executable..." -ForegroundColor Green
        Invoke-Expression "pyinstaller --noconfirm --onefile --windowed --name `"Notepad`" $IconFlag Notepad.py"
        Write-Host "Build complete: dist/Notepad.exe" -ForegroundColor Green
    }
    "linux" {
        Write-Host "Building Linux executable..." -ForegroundColor Green
        Invoke-Expression "pyinstaller --noconfirm --onefile --windowed --name `"Notepad`" $IconFlag Notepad.py"
        Write-Host "Build complete: dist/Notepad" -ForegroundColor Green
    }
}
