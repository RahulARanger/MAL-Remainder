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

write-output "here"

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

write-output $mode

switch($mode){
     1{ 
        $pythonZip = Join-Path -Path $ScriptPath -ChildPath "python.zip";
        Expand-Archive -Path $pythonZip -DestinationPath $PythonPath;
        Remove-Item -Path $pythonZip;
     }

     2{
        $pipFile = Join-Path -Path $ScriptPath -ChildPath "get-pip.py";
        & $executable $pipFile;
        Remove-Item -Path $pipFile;
     }

     3{
         $sitePath = Get-ChildItem -Path $PythonPath -Filter "*._pth"
         Set-Content -Path $sitePath.FullName -Value "
Lib
Lib/site-packages
.
import site
"
         $sitePath = Join-Path -Path $PythonPath -ChildPath "sitecustomize.py"
         if(Test-Path -Path $sitePath) {Remove-Item -Path $sitePath} else {}
         New-Item -Path $sitePath -ItemType "file"
         
         Set-Content -Path $sitePath -Value "
import sys;
import sys;
sys.path = sys.path[: 3]
"}

     4{
        $internalModules = (Get-ChildItem -Path $PythonPath -Filter "*.zip")
        $unzipped = Join-Path -Path $PythonPath -ChildPath "Lib"
    
        Expand-Archive -Path $internalModules.FullName -DestinationPath $unzipped
        Remove-Item -Path $internalModules.Fullname
     }

     5{
        $requirements = Join-Path -Path (Join-Path -Path $ScriptPath -ChildPath "ProjectAnalysis") -ChildPath "requirements.txt";
        if (Test-Path -Path $requirements) {& $executable @("-m", "pip", "install", "-r", $requirements)} else {}
     }
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

