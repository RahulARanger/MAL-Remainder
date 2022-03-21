<#
.SYNOPSIS
    MALRemainder CMDLine, Has four options, which are performed linearly as the order given below

.DESCRIPTION
    MALRemainder requires the user to set the tokens, 

.PARAMETER settings
    The Settigns

#>
param(
    [switch]$help,
    [Parameter(Position=0)] [switch]$re_ouath,
    [Parameter(Position=1)] [switch]$refresh_tokens,
    [Parameter(Position=2)] [switch]$refresh_abouts,
    [Parameter(Position=3)] [switch]$settings
)





if($help.IsPresent){
    if($re_ouath.IsPresent -or $refresh_tokens.IsPresent -or $settings.IsPresent -or $refresh_abouts.IsPresent){
        Write-Warning "All other options are ignored when help is present"
    }
    Get-Help -ShowWindow "./setup.ps1"
    Exit
}

