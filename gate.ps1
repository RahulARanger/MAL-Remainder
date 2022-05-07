<#
.SYNOPSIS
    MAL-Remainder reminds you to update the Number of episodes that is in your watch-list in MyAnimeList.
    After Updating it, it would reflect in MyAnimeList website. The Triggers are based on the events set in the given
    Google Calendar file

.DESCRIPTION
    Welcome to MAL Remainder.

    if you want to get started, you need to make sure

    1. you have MAL API Client ID and Client Secret which you can get from "web" type API.
    Refer this blog for clearing first step: https://myanimelist.net/blog.php?eid=835707

    2. make sure to use Google Calendar, which enables you to create your own schedule easily. [NOT IMPLEMENTED YET]
    

.PARAMETER help
    Displays this message and then exits

.PARAMETER sch
    Again, its internally used by the Scripts in order to let the application use the system's Scheduler. 
    Don't use it manually, you can always use TaskScheduler in your own system which is way more better than this.

.PARAMETER settings
    Opens the Server with the settings page opened instead of the home page which is not default thing to do

.PARAMETER deset
    Called while uninstalling application to remove the task of the name "MAL-Remainder" from the Task Scheduler

.PARAMETER sch
    Adds an Action "MAL-Remainder" to the Task Scheduler whose triggers are called once at the time passed as comma seperated values in arguments

.PARAMETER evil
    Called while Uninstalling this application, It clearly shows the uninstallation process.

.PARAMETER update
    Checks the latest version of the application and if there is a newer version, it will download it and install it.

.PARAMETER arguments
    Mostly used in combination with switch parameters for instance,
    * sch - Comma separated values of datetime to be used as triggers

#>
param(
    [switch]$help,
    [switch]$open,
    [switch]$settings,
    [switch]$deset,
    [switch]$sch,
    [switch]$set,
    [switch]$evil,
    [switch]$update,
    [String[]]$arguments
)

$DebugPreference = 'Continue'
$ErrorActionPreference = "Stop"

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
$MAL = Join-Path -Path $ScriptPath -ChildPath "MAL_Remainder"


function Get-RunningProjects{
    $Pythons = Join-Path -Path $PythonPath -ChildPath "*";
    return  Get-WmiObject -Class "Win32_Process" -ComputerName "." | where-object {$_.Path -like $Pythons};
}


function Get-ProjectPyPath{
    param(
        [string]$file
    )
    return "./MAL_Remainder/$file.py "
}

function Start-PythonScript{
    param(
        [String]$file="settings",
        [String[]]$arg_s=@()
    )

    $arg_s = (Get-ProjectPyPath -file $file) + $arg_s
    Start-Process $executable -WindowStyle Minimized -WorkingDirectory $ScriptPath -ArgumentList ($arg_s -Join " ")
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
    $action = New-ScheduledTaskAction -Execute $executable -WorkingDirectory $ScriptPath -Argument '"MAL_Remainder//settings.py" -automatic'
    # Creating Triggers from the time stamps
    if(-not $arguments[0]){
        return
    }

    $action_triggers = $arguments[0].Split(",") | ForEach-Object {
        New-ScheduledTaskTrigger -Once -At (Get-Date $_)
    }
    
    # Running only if connected to network and doesn't matter if your pc is on battery or on charge
    # by default, it has low priority
        $settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable -DontStopIfGoingOnBatteries -WakeToRun -AllowStartIfOnBatteries
    
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

function Get-Update{
        
    $response = Invoke-RestMethod -Uri "https://api.github.com/repos/RahulARanger/MAL-Remainder/releases/latest" -Method "GET"
    $update_it = $response.tag_name -ne $Matches.1

    if (-not $update_it){
        return
    }


    $download_url = $response.assets.browser_download_url
    $temp = Join-Path -Path $env:TEMP -ChildPath $response.assets.Name
    write-Output $temp

    Invoke-WebRequest -Uri $download_url -OutFile $temp

    Start-Process -FilePath $temp -Wait
    Remove-Item -Path $temp

    
}


switch($true){
    {$open.IsPresent}{
        Start-PythonScript -arguments @("automatic");
    }

    {$settings.IsPresent}{
        Start-PythonScript -file "settings" -arguments @("manual", "settings");
    }

    {$deset.IsPresent}{
        UnRegister-Remainder;
    }
    
    {$set.IsPresent}{
        Start-PythonScript -file "calendar_parse"
    }

    {$sch.IsPresent}{
        Deploy-Remainder
    }
    
    {$evil.IsPresent}{
        Write-Debug "Removing Python Directory"
        $host.UI.RawUI.WindowTitle = "Don't close this window, Closing this would affect the uninstallation process."
        Write-Debug "Collecting INFO..."
        
        
        $collected = Get-ChildItem -Path "python" -Recurse -File | ForEach-Object {$_.FullName}
        
        $index = 0
        $total = $collected.Length
        foreach ($file in $collected) {
            Remove-Item -path $file -Force
            $index += 1;
            Write-Progress -Activity "Removing Components of Python...`nDeleted:$file" -Status "Deleted Files $index / $total" -PercentComplete (($index / $total) * 100)
        }

        Write-Debug "Completed..."
    }

    {$update.IsPresent}{
        Write-Debug "Checking for any updates";
        ((Get-Content -Path (Join-Path -Path $MAL -ChildPath "__init__.py") -Raw) -match '^__version__\s?=\s?"(.*)"') |
            Get-Update
    }

    Default{
        $store = @(Get-RunningProjects);
        if($store.length -gt 0){$store | Out-GridView -passthru -Title "These processes must be closed in-order to proceed forward!"}
        if($store.length -gt 0){exit 5} else {}
    }
}

$DebugPreference = 'SilentlyContinue'
$ErrorActionPreference = "Continue"
