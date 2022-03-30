#include "misc_utils.iss"

#define Name="MALRemainder"
#define Repo="https://github.com/RahulARanger/MAL-Remainder"
#define Author="RahulARanger"
#define Version="0.5.0"
#define Mutex="Mal-Remainder"

[Setup]
; Basic Meta
AppName="{#Name}"
AppVersion="{#Version}"
AppPublisher="{#Author}"
AppPublisherURL="{#Repo}"
AppSupportURL="{#Repo}"
AppUpdatesURL="{#Repo}"
AppContact="{#Repo}"


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
SetupMutex={#Mutex}
AppMutex={#Mutex}

InfoBeforeFile="README.rtf"

; Below Value is Oberserved Value
ExtraDiskSpaceRequired=58576896 



[Files]
Source: "{tmp}\python.zip"; DestDir: "{app}"; flags: external skipifsourcedoesntexist; Permissions: users-modify;
Source: "{tmp}\get-pip.py"; DestDir: "{app}"; flags: external skipifsourcedoesntexist; Permissions: users-modify;
Source: "./setup.ps1"; DestDir: "{app}"; Permissions: users-modify;
Source: "../requirements.txt"; DestDir: "{app}"; Flags: deleteafterinstall; Permissions: users-modify; AfterInstall: PostInstall


; don't delete this ps1 file, it does some reliable work
Source: "../gate.ps1"; DestDir: "{app}";
Source: "../setup.cmd"; DestDir: "{app}";

Source: "../MAL_Remainder\templates\*"; DestDir: "{app}/MAL_Remainder/templates";
Source: "../MAL_Remainder\static\*"; DestDir: "{app}/MAL_Remainder/static"; Excludes: "Profile.jpg";
Source: "../MAL_Remainder\*"; DestDir: "{app}/MAL_Remainder";


[Dirs]
Name: "{app}/MAL_Remainder"; Permissions: everyone-modify;

; For more quality progress while uninistalling
Name: "{app}/python"; Permissions: everyone-full;
Name: "{app}/python/__pycache__"; Permissions: everyone-modify;
Name: "{app}/python/scripts"; Permissions: everyone-full;
Name: "{app}/python/pip"; Permissions: everyone-modify;

Name: "{app}/python/Lib/asyncio";
Name: "{app}/python/Lib/collections";
Name: "{app}/python/Lib/concurrent";
Name: "{app}/python/Lib/ctypes";
Name: "{app}/python/Lib/curses";
Name: "{app}/python/Lib/dbm";
Name: "{app}/python/Lib/distutils";
Name: "{app}/python/Lib/email";
Name: "{app}/python/Lib/encodings";
Name: "{app}/python/Lib/html";
Name: "{app}/python/Lib/http";
Name: "{app}/python/Lib/importlib";
Name: "{app}/python/Lib/json";
Name: "{app}/python/Lib/lib2to3";
Name: "{app}/python/Lib/logging";
Name: "{app}/python/Lib/msilib";
Name: "{app}/python/Lib/multiprocessing";
Name: "{app}/python/Lib/pydoc_data";
Name: "{app}/python/Lib/sqlite3";
Name: "{app}/python/Lib/unittest";
Name: "{app}/python/Lib/urllib";
Name: "{app}/python/Lib/wsgiref";
Name: "{app}/python/Lib/xml";
Name: "{app}/python/Lib/xmlrpc";



[UninstallDelete]
; files which have been skipped must be explicitly mentioned in this section 
Type: filesandordirs; Name: "{app}\python";

Type: files; Name: "{app}\requirements.txt";
Type: files; Name: "{app}\setup.ps1";
Type: files; Name: "{app}\get-pip.py";  
Type: files; Name: "{app}\python.zip";
Type: files; Name: "{app}\python\lib\*.pyc";

Type: filesandordirs; Name: "{app}\MAL_Remainder\__pycache__";
Type: filesandordirs; Name: "{app}\MAL_Remainder\data";

Type: filesandordirs; Name: "{app}\python\scripts\*.exe";

[Icons]
Name: "{group}\MAL-Remainder"; Filename: "{app}/setup.cmd"; Parameters: "-mode 6"; WorkingDir: "{app}"; Comment: "Remainder for your AnimeList"; Flags: runminimized


[Code]
// https://stackoverflow.com/questions/28221394/proper-structure-syntax-for-delphi-pascal-if-then-begin-end-and

// we start with this event
procedure InitializeWizard;
begin
  Ask := True;
  ImplicitExitCode := -1073741510

  DownloadPage := CreateDownloadPage('Downloading Python...', 'Downloading & Extracting Embedded python 3.8.9.zip', @OnDownloadProgress);
end;
                                    
function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  if CheckAndQuit() <> 0 then 
    Result := 'Please Close the necessary running applications to proceed forward'
  else 
    Result := CheckAndDownloadPython();
end;

procedure CurStepChanged(CurStep: TSetupStep);

begin
  if CurStep = ssPostInstall then 
    PostInstall;
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
      MsgBox('Please close the necessary applications before uninstalling this application!', mbError, MB_OK);

end;      