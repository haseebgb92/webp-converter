@echo off
echo Building WebP Converter MSI Installer...

REM Check if WiX toolset is installed
where candle >nul 2>&1
if %errorlevel% neq 0 (
    echo WiX toolset is not installed or not in PATH
    echo Please install WiX toolset from https://wixtoolset.org/releases/
    exit /b 1
)

REM Build the executable first
call venv\Scripts\activate
pyinstaller build_exe.spec

REM Build the MSI
echo Building MSI...
candle installer.wxs
if %errorlevel% neq 0 (
    echo Failed to compile WiX source
    exit /b 1
)

light -ext WixUIExtension installer.wixobj
if %errorlevel% neq 0 (
    echo Failed to link WiX objects
    exit /b 1
)

echo MSI installer created successfully!
echo You can find the installer at: installer.msi
