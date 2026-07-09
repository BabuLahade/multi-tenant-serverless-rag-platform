$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path "$PSScriptRoot\.."

$lambdaRoot = Join-Path $projectRoot "lambda"

$packageRoot = Join-Path $lambdaRoot "packages"

if (!(Test-Path $packageRoot)) {
    New-Item -ItemType Directory -Path $packageRoot | Out-Null
}

$functions = @(
    "nova_chat",
    "nova_crawl",
    "nova_ingest",
    "nova_authorizer"
)

foreach ($function in $functions) {

    Write-Host ""
    Write-Host "Building $function..." -ForegroundColor Cyan

    $temp = Join-Path $env:TEMP $function

    if (Test-Path $temp) {
        Remove-Item $temp -Recurse -Force
    }

    New-Item -ItemType Directory $temp | Out-Null

    Copy-Item "$lambdaRoot\$function\*" $temp -Recurse

    Copy-Item "$lambdaRoot\shared" $temp -Recurse

    $zipName = $function.Replace("_","-") + ".zip"

    $zipPath = Join-Path $packageRoot $zipName

    if (Test-Path $zipPath) {
        Remove-Item $zipPath
    }

    Compress-Archive `
        -Path "$temp\*" `
        -DestinationPath $zipPath

    Remove-Item $temp -Recurse -Force

    Write-Host "$zipName created." -ForegroundColor Green
}

Write-Host ""
Write-Host "All Lambda packages built successfully." -ForegroundColor Yellow