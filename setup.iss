[Setup]
AppName=SSH Manager
AppVersion=1.0
DefaultDirName={pf}\SSH Manager
DefaultGroupName=SSH Manager
OutputDir=.
OutputBaseFilename=ssh-manager-setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SSH Manager"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "Launch SSH Manager"; Flags: nowait postinstall skipifsilent