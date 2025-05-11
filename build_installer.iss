[Setup]
AppName=NEO Explorer
AppVersion=1.0
DefaultDirName={autopf}\NEO Explorer
OutputDir=installer
OutputBaseFilename=NEOExplorer_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "NEOExplorer.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\NEO Explorer"; Filename: "{app}\NEOExplorer.exe"
Name: "{commondesktop}\NEO Explorer"; Filename: "{app}\NEOExplorer.exe"