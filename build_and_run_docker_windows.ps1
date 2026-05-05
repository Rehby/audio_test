<#
PowerShell helper to ensure Docker Desktop is installed on Windows,
build the `audio-to-text` image from this repo (if `Dockerfile` exists),
and run the container.

Usage (PowerShell as admin recommended):
  .\build_and_run_docker_windows.ps1 [-ImageName audio-to-text] [-Port 8501] [-Build]

Notes:
- The script will try to elevate itself to Administrator if not already elevated.
- It attempts to download Docker Desktop for the detected architecture (x64/arm64).
- Silent install behaviour depends on the Docker installer version; if automatic install fails,
  the interactive installer will launch and you must finish installation manually.
#>

param(
    [string]$ImageName = 'audio-to-text',
    [int]$Port = 8501,
    [switch]$Build = $true
)

function Is-Administrator {
    $current = [Security.Principal.WindowsIdentity]::GetCurrent()
    (New-Object Security.Principal.WindowsPrincipal($current)).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Is-Administrator)) {
    Write-Host "Restarting script elevated (Administrator required for Docker Desktop install)..."
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = 'powershell.exe'
    $psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Definition)`""
    $psi.Verb = 'runas'
    try { [System.Diagnostics.Process]::Start($psi) | Out-Null; exit } catch { Write-Error "Elevation cancelled."; exit 1 }
}

function Test-DockerAvailable {
    try {
        docker version --format '{{.Server.Version}}' > $null 2>&1
        return $true
    } catch {
        return $false
    }
}

function Wait-ForDocker {
    param([int]$TimeoutSeconds = 120)
    $start = Get-Date
    while ((Get-Date) -lt $start.AddSeconds($TimeoutSeconds)) {
        if (Test-DockerAvailable) { return $true }
        Start-Sleep -Seconds 3
    }
    return $false
}

if (-not (Test-DockerAvailable)) {
    Write-Host "Docker not found. Attempting to download and install Docker Desktop..."

    $arch = (Get-CimInstance Win32_OperatingSystem).OSArchitecture
    if ($arch -like '*ARM*') {
        $installerUrl = 'https://desktop.docker.com/win/stable/arm64/Docker%20Desktop%20Installer.exe'
    } else {
        $installerUrl = 'https://desktop.docker.com/win/stable/amd64/Docker%20Desktop%20Installer.exe'
    }

    $installerPath = Join-Path $env:TEMP 'DockerDesktopInstaller.exe'
    Write-Host "Downloading Docker Desktop from $installerUrl to $installerPath"
    try {
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing -TimeoutSec 300
    } catch {
        Write-Error "Failed to download Docker Desktop installer: $_"
        exit 2
    }

    Write-Host "Running installer. This may prompt you to accept agreements and may take a few minutes..."
    try {
        # Many Docker Desktop installers support unattended switches; if not, the interactive installer will run.
        $proc = Start-Process -FilePath $installerPath -ArgumentList '--quiet' -Wait -PassThru -ErrorAction SilentlyContinue
        if ($proc -eq $null) {
            # Fallback: run without args
            Start-Process -FilePath $installerPath -Wait
        }
    } catch {
        Write-Warning "Installer returned an error; you may need to finish installation interactively. Error: $_"
    }

    Write-Host "Waiting for Docker daemon to become available..."
    if (-not (Wait-ForDocker -TimeoutSeconds 300)) {
        Write-Error "Docker did not become available within timeout. Please start Docker Desktop manually and re-run this script."
        exit 3
    }
}

Write-Host "Docker is available. Version:"
docker --version

Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)

if ($Build -and (Test-Path -Path './Dockerfile')) {
    Write-Host "Building Docker image '$ImageName' from Dockerfile..."
    & docker build -t $ImageName .
    if ($LASTEXITCODE -ne 0) { Write-Error "docker build failed (exit $LASTEXITCODE)"; exit $LASTEXITCODE }
} elseif ($Build) {
    Write-Warning "No Dockerfile found in repository root; skipping build. If you want to run a prebuilt image, set -Build:$false and ensure image exists locally or on a registry."
}

Write-Host "Running container '$ImageName' mapping host port $Port -> container port 8501..."

# Create local cache dir for huggingface models (optional)
$cacheHost = Join-Path $PWD '.cache\huggingface'
if (-not (Test-Path $cacheHost)) { New-Item -ItemType Directory -Path $cacheHost | Out-Null }

Write-Host "Starting docker run (press Ctrl+C to stop)..."
try {
    & docker run --rm -p $Port`:8501 -v "${cacheHost}:/root/.cache/huggingface" $ImageName
    exit $LASTEXITCODE
} catch {
    Write-Error "Failed to start container: $_"
    exit 4
}
