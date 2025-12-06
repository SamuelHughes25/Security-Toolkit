# Shared functions for S&M Toolkit

function Write-Log {
    param([string]$msg)
    Add-Content "$env:TEMP\SM-Toolkit.log" "[$(Get-Date)] $msg"
}

function Load-Tools {
    return Get-Content "$PSScriptRoot\tools.json" | ConvertFrom-Json
}

function Download-File {
    param($Url, $Destination)

    Write-Log "Downloading $Url"
    Invoke-WebRequest -Uri $Url -OutFile $Destination -UseBasicParsing
}

function Install-Tool {
    param($Tool)

    $tempPath = "$env:TEMP\$($Tool.name).exe"

    Download-File $Tool.url $tempPath

    if ($Tool.silent) {
        Start-Process $tempPath -ArgumentList $Tool.silent -Wait
    } else {
        Start-Process $tempPath -Wait
    }

    Write-Log "Installed $($Tool.name)"
}
