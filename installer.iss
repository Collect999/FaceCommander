; Script originally generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
;
; Reference documentation for #define, #pragma and other Inno Setup
; preprocessor directives is near here. https://jrsoftware.org/ispphelp/
; See also.
; -   Direct link to documentation of the ReadIni() built-in function.
;     https://documentation.help/Inno-Setup-Preprocessor-ISPP/topic_readini.htm
; -   SO answer about use of SourcePath to generate a full path.
;     https://stackoverflow.com/a/15288570/7657675

#define MyAppName "FaceCommander"
#define MyAppExeName "FaceCommander.exe"
#define VersionIniPath \
    AddBackSlash(SourcePath) + AddBackSlash("assets") + "Version.ini"
#define VersionIniSection "Release"
#define VersionIniKey "VersionNumber"

#pragma message \
    "VersionIniPath '" + VersionIniPath + "' " \
    + (FileExists(VersionIniPath) ? "Exists" : "Doesn't exist") + "."
#define IniVersion ReadIni(VersionIniPath, VersionIniSection, VersionIniKey)
;
; Note that a default isn't specified so that the Inno Setup Compiler will fail
; if the value isn't read from the INI file for any reason. The error is like
; this.
;
;     Compiler Error
;     The [Setup] section must include an AppVersion or AppVerName directive.
;
#pragma message "IniVersion '" + IniVersion + "'"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{B266B614-4113-4DB7-9A30-4250FECA5009}
AppName={#MyAppName}
AppVersion={#IniVersion}
;AppVerName={#MyAppName} {#IniVersion}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename=FaceCommander-Installer-v{#IniVersion}
SetupIconFile=assets\images\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";
Name: "autostarticon"; Description: "{cm:AutoStartProgram,{#MyAppName}}"; GroupDescription: "{cm:AdditionalIcons}";


[Files]
Source: "dist\facecommander\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\facecommander\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Parameters: "/auto"; Tasks: autostarticon
; Name: "{commonstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Parameters: "/auto"; Tasks: autostarticon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Verb: runas; Flags: postinstall skipifsilent shellexec runascurrentuser waituntilterminated; 

