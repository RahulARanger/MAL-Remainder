<#
.SYNOPSIS
    MALRemainder, just open the application to force the remainder. it doesn't affect your usual schedule, but might affect the data that it migth collect in the future.
    It is not recommended to use this CMDLINE feature for now.

.DESCRIPTION
    Welcome to MAL Remainder. As a remainder.

    if you want to get started, you need to make sure

    1. you have MAL API Client ID and Client Secert which you can get from "web" type API.
    Refer this blog for clearing first step: https://myanimelist.net/blog.php?eid=835707

    2. make sure to use Google Calendar, which enabels you to create your own schedule easily. [NOT IMPLEMENTED YET]
    

.PARAMETER help
    Displays this message and then exits

.PARAMETER mode
    Internally used by the Scripts in order to perform Installations or the Uninstallations
    or to open the main application, anyways its something that one mustn't use manually

.PARAMETER sch
    Again, its internally used by the Scripts in order to let the application use the system's Scheduler. 
    Don't use it manually, you can always use TaskScheduler in your own system which is way more better than this.

.PARAMETER settings
    Opens the Server with the settings page opened instead of the home page which is not default thing to do

#>
param(
    [switch]$help,
    [switch]$sch,
    [switch]$settings,
    [switch]$dashboard,
    [String[]]$triggers_for_end,
    [int]$mode=0
)

if($help.IsPresent){
    Write-Warning "If Executed with some other arguments, it's ignored with the -help option"
    Get-Help -ShowWindow $MyInvocation.MyCommand.Definition
    Exit;
}


# Some Static Constants

$TaskName = "MAL-Remainder"
$TaskDescription = "Remainder for updating your watch status regularly or maybe used to remind you to take a break before hand"


# Some Dynamic Constants

$ScriptPath = (Get-Location).Path
$PythonPath = Join-Path -Path $ScriptPath -ChildPath "Python";
$executable = Join-Path -Path $PythonPath -ChildPath "python.exe";


function Get-RunningProjects{
    $Pythons = Join-Path -Path $PythonPath -ChildPath "*";
    return  Get-WmiObject -Class "Win32_Process" -ComputerName "." | where-object {$_.Path -like $Pythons};
}


function Start-PythonScript{
    param(
        [String]$file="settings",
        [String[]]$arguments=@()
    )

    $arguments = "./MAL_Remainder/$file.py " + $arguments
    Start-Process $executable -WindowStyle Minimized -WorkingDirectory $ScriptPath -ArgumentList ($arguments -Join " ")
}


function Get-UserName{
    # format: <host-name>\<user-name>
    # host-name has alphanumeric, hyphen only
    
    # Most secured way: https://stackoverflow.com/a/29955210/12318454
    $user = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
    return $user.SubString($user.indexOf("\") + 1) 
}


function Deploy-Remainder{

    # Task = Action + Trigger(s) + Settings + Prinicpal
    # Task = "What to do" + "When to do" + "With some config." + "for whom we need to do, security things"
    
    $action = New-ScheduledTaskAction -Execute (Join-Path -Path $ScriptPath -ChildPath "setup.cmd") -WorkingDirectory $ScriptPath -Argument "-mode 6"

    # Creating Triggers from the time stamps
    $action_triggers = $triggers_for_end | % {
        New-ScheduledTaskTrigger -Once -At (Get-Date $_)
    }
    
    # Running only if connected to network
    $settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable
    
    # Using the Local. Currently Signed Account UserName
    $principal =  New-ScheduledTaskPrincipal  -UserId (Get-UserName) -LogonType ServiceAccount

    # -Force if already Task Exists, Deletes the Old one by replacing with the new one
    Register-ScheduledTask -TaskName $TaskName -Description $TaskDescription -Action $action -Trigger $action_triggers -Settings $settings -Principal $principal -Force
}



function UnRegister-Remainder{
    $Task = Get-ScheduledTask | Where-Object {$_.TaskName -like $TaskName }

    if(-not $Task){
        Write-Output "Not Registered in the first place"
        return 
    }
    Unregister-ScheduledTask -InputObject $Task -Confirm:$false
    
}

switch($true){
{$sch.IsPresent}{
    $mode = 8;
}
{$settings.IsPresent}{
    $mode = 7;
}
}

switch($mode){
     6{
        Start-PythonScript -arguments @("automatic");
     }

     7{
         Start-PythonScript -file "settings" -arguments @("-manual", "settings");
     }

     8{
        Deploy-Remainder
     }
     9{
         # TODO: Create a Dash Board for the MAL - Remainder
     }

     10{
        Start-PythonScript -file "calendar_parse"
    }

    11{
        # Make sure to run this with Admin Rights
        UnRegister-Remainder
        
    }

     Default{
        $store = @(Get-RunningProjects);
        if($store.length -gt 0){$store | Out-GridView -passthru -Title "These processes must be closed in-order to proceed forward!"}
        if($store.length -gt 0){exit 5} else {}  # exiting with the bad mood 😤

     }
}

# if CurPageID <> 1 then begin
#   // don't check before evening starting that's BAD ðŸ¥²
#   CheckRunning(False);
#   end;


# function CheckRunning(FromUninstaller: Boolean): Boolean;
# var 
# AppDir: String;
# begin
#   Result := True;
#   if FromUninstaller then
#     AppDir := ExpandConstant('{app}') 
#   else
#     AppDir := WizardDirValue();
  
#   if not ShellExec(Format('-ExecutionPolicy ByPass -File "%s\gate.ps1" -Mode 0', [AppDir]), AppDir) then 
#   begin
   
#     if not FromUninstaller then
#       CloseSetup('Application is Running in background, check the processes and close them and try again!')
#       // raises Null Pointer Exception in case of the Uninstaller
#     else
#       MsgBox('MAL-Remainder is Running, Please close them and try again!', mbError, MB_OK);
#     Result := False;
#   end;
# end;