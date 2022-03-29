$DebugPreference = 'Continue'
$ErrorActionPreference = "Stop"


$host.UI.RawUI.WindowTitle = "Don't close this window, close this to stop the setup"

$ScriptPath = (Get-Location).Path 
$PythonPath = Join-Path -Path $ScriptPath -ChildPath "Python";
$executable = Join-Path -Path $PythonPath -ChildPath "python.exe";

# Extracting Embedded Python, NOTE: this assumes Innosetup has already 
$temp_file = Join-Path -Path $ScriptPath -ChildPath "python.zip"

if(Test-Path -Path $temp_file){
    Write-Debug "Extracting Embedded Package"
    Expand-Archive -Path $temp_file -DestinationPath $PythonPath;
    Remove-Item -Path $temp_file;
}

# Installs Pip
$temp_file = Join-Path -Path $ScriptPath -ChildPath "get-pip.py";

if(Test-Path -Path $temp_file){
    Write-Debug "Installing and setting Pip up..."
    & $executable $temp_file;
    Remove-Item -Path $temp_file;   
}

# This enables python to use Lib and site-packages inside it, so the one we install through pip
$temp_file = Get-ChildItem -Path $PythonPath -Filter "*._pth"
Set-Content -Path $temp_file.FullName -Value "
Lib
Lib/site-packages
../
.
import site
"

# creates a site-customize.py, which enables python Interpreter know the sys.path
# we also make sure to not use any pre-existing python paths
$temp_file = Join-Path -Path $PythonPath -ChildPath "sitecustomize.py"
if(Test-Path -Path $temp_file) {Remove-Item -Path $temp_file} else {}

New-Item -Path $temp_file -ItemType "file"
Set-Content -Path $temp_file -Value "
import sys;
sys.path = sys.path[: 4]
"

# Now we unzip the internal Modules, we do that so we can use mostly all of them without any problem
$temp_file = (Get-ChildItem -Path $PythonPath -Filter "*.zip")


if($temp_file -and (Test-Path -Path $temp_file[0].FullName)){
    $unzipped = Join-Path -Path $PythonPath -ChildPath "Lib"
    Expand-Archive -Path $temp_file.FullName -DestinationPath $unzipped 
    Remove-Item -Path $temp_file.Fullname
}

# Now we install external packages for the build from requirements.txt
$temp_file = Join-Path -Path $ScriptPath -ChildPath "requirements.txt";
if (Test-Path -Path $temp_file) {& $executable @("-m", "pip", "install", "-r", $temp_file)} else {}

Write-Output "Installation is over"

$DebugPreference = 'SilentlyContinue'
$ErrorActionPreference = "Continue"
