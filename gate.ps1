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

.PARAMETER sch
    Again, its internally used by the Scripts in order to let the application use the system's Scheduler. 
    Don't use it manually, you can always use TaskScheduler in your own system which is way more better than this.

.PARAMETER settings
    Opens the Server with the settings page opened instead of the home page which is not default thing to do

#>
param(
    [switch]$help,
    [switch]$open,
    [switch]$settings,
    [switch]$ask,
    [switch]$deset,
    [switch]$sch,
    [switch]$set,
    [switch]$evil,
    [String[]]$arguments
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


function Get-ProjectPyPath{
    param(
        [string]$file
    )
    return "./MAL_Remainder/$file.py "
}

function Start-PythonScript{
    param(
        [String]$file="settings",
        [String[]]$arguments=@()
    )

    $arguments = (Get-ProjectPyPath -file $file) + $arguments
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
    
    $action = New-ScheduledTaskAction -Execute (Join-Path -Path $ScriptPath -ChildPath "setup.cmd") -WorkingDirectory $ScriptPath -Argument "-open"

    # Creating Triggers from the time stamps
    $action_triggers = $arguments | ForEach-Object {
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


function Show-Top{
    $signature = @'
[DllImport("user32.dll")]
public static extern bool SetWindowPos(
    IntPtr hWnd,
    IntPtr hWndInsertAfter,
    int X,
    int Y,
    int cx,
    int cy,
    uint uFlags);
'@

    $type = Add-Type -MemberDefinition $signature -Name SetWindowPosition -Namespace SetWindowPos -Using System.Text -PassThru

    $handle = (Get-Process -id $Global:PID).MainWindowHandle
    $alwaysOnTop = New-Object -TypeName System.IntPtr -ArgumentList (-1)
    $type::SetWindowPos($handle, $alwaysOnTop, 0, 0, 0, 0, 0x0003)
}


function Ask-Settings{
write-output "asked"
    Add-Type -AssemblyName PresentationFramework
    # https://docs.microsoft.com/en-us/dotnet/api/microsoft.win32.openfiledialog?view=windowsdesktop-6.0
    $Dialog = New-Object Microsoft.Win32.OpenFileDialog
    $Dialog.DefaultExt=".db"
    $Dialog.Filter="sqlite3-DB (.db)|*.db"
    $Dialog.Title="Select Setting.db"
    $Dialog.CheckFileExists=$true
    $Dialog.CheckPathExists=$true
    $Dialog.FileName = "settings"
    $Dialog.Multiselect=$false

    Show-Top

    if($Dialog.ShowDialog() -eq $true){
        return $Dialog.FileName
    }
    return ""
}

switch($true){
    {$open.IsPresent}{
        Start-PythonScript -arguments @("automatic");
     }

    {$settings.IsPresent}{
        Start-PythonScript -file "settings" -arguments @("-manual", "settings");
    }
    
    {$ask.IsPresent}{
        $asked = Ask-Settings
        if (-not ($asked -eq "")) {& $executable (Get-ProjectPyPath -file "import_settings") $asked} else {}
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
            Write-Progress -Activity "Removing Components of Python..." -Status "Deleted Files $index / $total" -PercentComplete (($index / $total) * 100)
        }

        Write-Debug "Completed..."
    }
     Default{
        $store = @(Get-RunningProjects);
        if($store.length -gt 0){$store | Out-GridView -passthru -Title "These processes must be closed in-order to proceed forward!"}
        if($store.length -gt 0){exit 5} else {}  # exiting with the bad mood 😤
     }
}
