; WebP Converter Installer Script
!include "MUI2.nsh"

; General
Name "WebP Converter"
OutFile "WebPConverter_Setup.exe"
Unicode True
InstallDir "$PROGRAMFILES\WebP Converter"
InstallDirRegKey HKCU "Software\WebP Converter" ""
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "icons\installer.ico"
!define MUI_UNICON "icons\installer.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.rtf"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Language
!insertmacro MUI_LANGUAGE "English"

Section "WebP Converter" SecMain
    SetOutPath "$INSTDIR"
    
    ; Add files
    File "dist\WebPConverter.exe"
    File /r "icons\*.*"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\WebP Converter"
    CreateShortcut "$SMPROGRAMS\WebP Converter\WebP Converter.lnk" "$INSTDIR\WebPConverter.exe" "" "$INSTDIR\icons\installer.ico"
    CreateShortcut "$DESKTOP\WebP Converter.lnk" "$INSTDIR\WebPConverter.exe" "" "$INSTDIR\icons\installer.ico"
    
    ; Write uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Write registry keys
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WebP Converter" \
                     "DisplayName" "WebP Converter"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WebP Converter" \
                     "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WebP Converter" \
                     "DisplayIcon" "$INSTDIR\icons\installer.ico"
SectionEnd

Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\WebPConverter.exe"
    RMDir /r "$INSTDIR\icons"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\WebP Converter\WebP Converter.lnk"
    Delete "$DESKTOP\WebP Converter.lnk"
    RMDir "$SMPROGRAMS\WebP Converter"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WebP Converter"
    DeleteRegKey HKCU "Software\WebP Converter"
    
    ; Remove installation directory
    RMDir "$INSTDIR"
SectionEnd
