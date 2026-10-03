#define MyAppName "GestureLock"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "GestureLock"
#define MyAppExeName "GestureLock.exe"

[Setup]
AppId={{8E7D4F7B-5B4B-4C71-A8E8-7F5E2B2A9C31}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\GestureLock
DefaultGroupName=GestureLock
OutputDir=installer
OutputBaseFilename=GestureLock-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayName=GestureLock
VersionInfoDescription=GestureLock Gesture-Based PC Security
VersionInfoProductName=GestureLock
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "dist\GestureLock\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\GestureLock"; Filename: "{app}\GestureLock.exe"
Name: "{autodesktop}\GestureLock"; Filename: "{app}\GestureLock.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\GestureLock.exe"; Description: "Launch GestureLock"; Flags: nowait postinstall skipifsilent