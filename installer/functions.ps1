# functions.ps1 - helper functions for S&M Toolkit installer

#---------------------------------------
# Download-Tool
# Downloads a tool from URL to specified folder
# Handles .exe and .msi
#---------------------------------------
function Download-Tool {
    param (
        [Parameter(Mandatory=$true)][string]$Url,
        [Parameter(Mandatory=$true)][string]$Destination
    )

    try {
        Invoke-WebRequest -Uri $Url -OutFile $Destination -UseBasicParsing
        Write-Host "Downloaded $Destination successfully"
        return $true
    } catch {
        Write-Host "Failed to download $Url"
        return $false
    }
}

#---------------------------------------
# Install-Tool
# Installs a tool silently based on type (exe/msi)
#---------------------------------------
function Install-Tool {
    param (
        [Parameter(Mandatory=$true)][psobject]$Tool,
        [Parameter(Mandatory=$true)][string]$InstallFolder
    )

    # Determine file extension from URL
    $uri = [System.Uri]$Tool.url
    $ext = [System.IO.Path]::GetExtension($uri.AbsolutePath)
    if ([string]::IsNullOrEmpty($ext)) { $ext = ".exe" }

    # Construct full path
    $installerPath = Join-Path $InstallFolder "$($Tool.name)$ext"

    # Download
    if (-not (Download-Tool -Url $Tool.url -Destination $installerPath)) {
        Write-Host "Skipping $($Tool.name) due to download failure"
        return $false
    }

    # Install silently
    try {
        if ($Tool.type -eq "msi") {
            Start-Process "msiexec.exe" -ArgumentList "/i `"$installerPath`" $($Tool.silent)" -Wait
        } else {
            Start-Process $installerPath -ArgumentList $Tool.silent -Wait
        }
        Write-Host "$($Tool.name) installed successfully"
        return $true
    } catch {
        Write-Host "Installation failed for $($Tool.name): $_"
        return $false
    }
}
