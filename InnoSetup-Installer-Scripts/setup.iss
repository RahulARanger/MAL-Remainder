#include "misc_utils.iss"

#define Version="0.7.8"
#define Name="MAL-Remainder"
#define Repo="https://github.com/RahulARanger/MAL-Remainder"
#define Author="RahulARanger"
#define Mx="Mal-Remainder"
#define SignTool="Sign"
#define OpenSettings = "../Mal_Remainder/settings.py manual settings"
#define RegularReSchedule = "../Mal_Remainder/calendar_parse.py"
#define ForceSchedule = "../Mal_Remainder/settings.py automatic"
#define PyRoot = "{app}/python"
#define DataLastRefreshed = "30-04-2022 14:41"

[Setup]
; Basic Meta
AppName="{#Name}"
AppVersion="{#Version}"
AppPublisher="{#Author}"
AppPublisherURL="{#Repo}"
AppSupportURL="https://rahularanger.github.io/MAL-Remainder"
AppUpdatesURL="{#Repo}/releases/latest"
AppContact="{#Repo}/issues"


BackColor=clBlue
BackColor2=clBlack


; IMPORTANT
AllowCancelDuringInstall=yes
; tho default yes, don't change this, else we won't be able to quit even if install fails I GUESS

; does it add some registry keys
ChangesEnvironment=yes  

; 64 Bit Application, this changes lot of constants like the fodler for {app} its in program files
; instead of programe files (x86)
; refer: https://jrsoftware.org/ishelp/topic_consts.htm
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; makes installer not fully resizable (it still has some max and min sizes)
WindowResizable=no

; Group Name on starts folder
DefaultGroupName="MAL-Remainder"                                                 

; Show Selected Directory
AlwaysShowDirOnReadyPage=yes
AppComments="Downloads Python requirements and others if any, for the MAL-Remainder"

; WHERE TO SAVE AFTER INSTALLATION
DefaultDirName="{autopf}\{#Name}"


OutputDir="Output"
OutputBaseFilename="{#Name}"

; uninstall exe file name 
UninstallDisplayName="Mal-Remainder-Uninstall"

; Compression Things
Compression=lzma
SolidCompression=yes

; Uses Windows Vista style
WizardStyle=modern

DisableWelcomePage=no
; This is the first page up until now, it just shows the LICENSE and makes sure user accepts it
LicenseFile="../LICENSE.txt"

; doesn't allow more than one setup to run at the same time
SetupMutex={#Mx}
AppMutex={#Mx}

InfoBeforeFile="README.rtf"

; Below Value is Oberserved Value
ExtraDiskSpaceRequired=40022016
ReserveBytes=58576896

; Comment this line if you want to locally setup
SignTool=SignThis



[Files]
Source: "{tmp}\python.zip"; DestDir: "{app}"; flags: external skipifsourcedoesntexist; Permissions: users-modify;
Source: "{tmp}\get-pip.py"; DestDir: "{app}"; flags: external skipifsourcedoesntexist; Permissions: users-modify;
Source: "./setup.ps1"; DestDir: "{app}"; Permissions: users-modify; Flags: deleteafterinstall;
Source: "../requirements.txt"; DestDir: "{app}"; Permissions: users-modify; AfterInstall: PostInstall

; don't delete this ps1 file, it does some reliable work
Source: "../gate.ps1"; DestDir: "{app}";
Source: "../setup.cmd"; DestDir: "{app}";

Source: "../MAL_Remainder\templates\*"; DestDir: "{app}/MAL_Remainder/templates";
Source: "../MAL_Remainder\static\*"; DestDir: "{app}/MAL_Remainder/static"; Excludes: "Data\*";
Source: "../MAL_Remainder\*"; DestDir: "{app}/MAL_Remainder";


[Dirs]
Name: "{app}/MAL_Remainder"; Permissions: everyone-modify;

; For more quality progress while uninistalling
Name: "{#PyRoot}"; Permissions: everyone-full;
Name: "{#PyRoot}/__pycache__"; Permissions: everyone-modify;
Name: "{#PyRoot}/scripts"; Permissions: everyone-full;
Name: "{#PyRoot}/pip"; Permissions: everyone-modify;


[UninstallDelete]
; files which have been skipped must be explicitly mentioned in this section 
Type: filesandordirs; Name: "{#PyRoot}";

Type: files; Name: "{app}\requirements.txt";
Type: files; Name: "{app}\setup.ps1";
Type: files; Name: "{app}\get-pip.py";  
Type: files; Name: "{app}\python.zip";
Type: files; Name: "{app}\python\lib\*.pyc";
Type: files; Name: "{app}\meta.ini";

Type: filesandordirs; Name: "{app}\MAL_Remainder\__pycache__";
Type: filesandordirs; Name: "{app}\MAL_Remainder\static\data";
Type: filesandordirs; Name: "{app}\MAL_Remainder\static";
Type: filesandordirs; Name: "{#PyRoot}\scripts\*.exe";

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Icons]
Name: "{autodesktop}\{#Name}"; Filename: "{#PyRoot}/python.exe"; Parameters: "{#ForceSchedule}"; WorkingDir: "{#PyRoot}"; Comment: "Remainder for your AnimeList"; Flags: runminimized; Tasks: desktopicon 
Name: "{autostartup}\{#Name}"; Filename: "{#PyRoot}/pythonw.exe"; Parameters: "{#RegularReSchedule}"; WorkingDir: "{#PyRoot}"; Comment: "Auto Fetches the Timings from Calendar and Schedules it in your Machine"; Flags: runminimized
Name: "{group}\{#Name}"; Filename: "{#PyRoot}/python.exe"; Parameters: "{#OpenSettings}"; WorkingDir: "{#PyRoot}"; Comment: "Opens up the settings of the Mal-Remainder"; Flags: runminimized


[Run]
// any other than powershell.exe will trigger false positive virus test.
Filename: "powershell.exe"; Description: "Open Settings for the MAL-Remainder"; Parameters: "-file ""{app}\gate.ps1"" -settings"; WorkingDir: "{app}"; Flags: postinstall runasoriginaluser runminimized


[INI]
Filename: "{app}\meta.ini"; Section: "Data"; Key: "Refreshed"; String: "{#DataLastRefreshed}"


[Code]
// https://stackoverflow.com/questions/28221394/proper-structure-syntax-for-delphi-pascal-if-then-begin-end-and

// we start with this event
procedure InitializeWizard;

begin
  Ask := True;
  ImplicitExitCode := -1073741510;
  Downloaded := True;
  DownloadPage := CreateDownloadPage('Downloading Python...', 'Downloading & Extracting Embedded python 3.8.9.zip', @OnDownloadProgress);

  DataOutDated := False;
end;
                                    
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  if CheckAndQuit() <> 0 then 
    Result := 'Please Close the necessary running applications to proceed forward'
  else 
    Result := CheckAndDownloadPython();
end;

// one needs to copy this event function as it is or modify them as they need
procedure CancelButtonClick(CurPageID: Integer; var Cancel, Confirm: Boolean);
begin
  Confirm := Confirm and Ask;
end;

function InitializeUninstall: Boolean;
begin
  Result := CheckAndQuit() = 0;

  if not Result then
      MsgBox('Please close the necessary applications before uninstalling this application!', mbError, MB_OK)
end;      

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
ResultCode: Integer;

begin
  if CurUninstallStep = usUninstall then
  begin
    ExecPSScript('gate.ps1', False, '-deset', ResultCode);
    // close this script to NOT see detailed progress
    ExecPSScript('gate.ps1', True, '-evil', ResultCode);
  end;
end;


Procedure CurStepChanged(CurStep: TSetupStep);
var
SavePath: String;
DataFile: String;
begin
  if CurStep = ssInstall then 
    begin 
      DataFile := ExpandConstant('{app}/meta.ini');
      DataOutDated := FileExists(DataFile) and (GetIniString('Data', 'Refreshed', '', DataFile) <> ExpandConstant('{#DataLastRefreshed}'));
    end;
      
  if CurStep = ssPostInstall then
    begin
      DataFile := ExpandConstant('{app}/MAL_Remainder/static/data/data.csv')
      
      if DataOutDated then
          begin 
            if (SuppressibleMsgBox('It seems that there was some changes in the Data Format.'#13#10''#13#10'Sorry for the inconvenience, We would now delete the old File.'#13#10'Would you like to Save before deleting this file ?', mbInformation, MB_YESNO or MB_SETFOREGROUND, IDYES) = IDYES) and GetSaveFileName('Save Data in', SavePath, '', 'Data Files (*.csv)', 'csv') then
              FileCopy(DataFile, SavePath, False);
            DeleteFile(DataFile);
          end;
    end;
end;