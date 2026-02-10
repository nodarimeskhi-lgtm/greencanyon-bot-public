$ErrorActionPreference = "Stop"
$nodeVersion = "v20.11.0"
$installDir = "$env:LOCALAPPDATA\node"
$zipUrl = "https://nodejs.org/dist/$nodeVersion/node-$nodeVersion-win-x64.zip"
$zipPath = "$env:TEMP\node.zip"

Write-Host "Installing Node.js $nodeVersion to $installDir..."

if (Test-Path $installDir) {
    Write-Host "Cleaning existing installation..."
    Remove-Item -Recurse -Force $installDir
}

Write-Host "Downloading $zipUrl..."
Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

Write-Host "Extracting..."
Expand-Archive -Path $zipPath -DestinationPath "$env:LOCALAPPDATA" -Force

# Rename extracted folder to 'node'
$extractedFolder = "$env:LOCALAPPDATA\node-$nodeVersion-win-x64"
Rename-Item -Path $extractedFolder -NewName "node"

# Set valid path for current session
$env:Path += ";$installDir"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$installDir", "User")

Write-Host "Node.js installed successfully."
node --version
npm --version
