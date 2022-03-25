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

#>
param(
    [switch]$help,
    [int]$mode=0,
    [switch]$sch
)


$ScriptPath = (Get-Location).Path
$PythonPath = Join-Path -Path $ScriptPath -ChildPath "Python";
$executable = Join-Path -Path $PythonPath -ChildPath "python.exe";

function Get-RunningProjects{
    $Pythons = Join-Path -Path $PythonPath -ChildPath "*";
    return  Get-WmiObject -Class "Win32_Process" -ComputerName "." | where-object {$_.Path -like $Pythons};
}
function Start-Remainder{
    param(
        [bool]$automatic=$true,
        [String]$route=""

    )

    $first = if($automatic){"automatic"} else {"manual"}
    
    $arguments = @(
        "./MAL_Remainder/settings.py", $first
    )
    if($automatic) {} else {$arguments += $route}
    write-output $arguments

    $python_path = "python.exe";
    Start-Process $python_path -WindowStyle Minimized -WorkingDirectory $ScriptPath -ArgumentList ($arguments -Join " ")

}

$mode = if($sch.IsPresent) {7} else {0};

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
        Start-Remainder;

     }

     7{
         Start-Remainder $false;
     }

     8{
         
     }
     9{
         Start-Remainder $false "dashboard";
        # TODO: Create a Dash Board for the MAL - Remainder
     }

     Default{
        $store = @(Get-RunningProjects);
        if($store.length -gt 0){$store | Out-GridView -passthru -Title "These processes must be closed in-order to proceed forward!"}
        if($store.length -gt 0){exit 5} else {}  # exiting with the bad mood 😤

     }
}
Start-Remainder