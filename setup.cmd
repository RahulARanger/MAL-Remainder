@echo off

REM Some commands need to be hidden but some doesn't need to

if %1 == -help (
    POWERSHELL -NoLogo -NoExit -ExecutionPolicy Bypass -File "./gate.ps1" -help
    GOTO END
)

if %1 == -ask (
    POWERSHELL -WindowStyle "Maximized" -NonInteractive -ExecutionPolicy Bypass -File "./gate.ps1" -ask
    GOTO END
)

POWERSHELL -ExecutionPolicy Bypass -File "./gate.ps1" %*
:END

@echo on
