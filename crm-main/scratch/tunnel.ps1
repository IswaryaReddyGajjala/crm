# PowerShell script to start localtunnel on port 8005 and extract the public URL
$logFile = Join-Path $PSScriptRoot "tunnel.log"
Remove-Item $logFile -ErrorAction SilentlyContinue

Write-Host "Starting localtunnel on port 8005..."
Start-Process -FilePath "cmd.exe" -ArgumentList "/c npx localtunnel --port 8005" -RedirectStandardOutput $logFile -NoNewWindow

# Wait and poll the log file for the URL
$tunnelUrl = ""
for ($i = 1; $i -le 15; $i++) {
    Start-Sleep -Seconds 1
    if (Test-Path $logFile) {
        $content = Get-Content $logFile
        Write-Host "Log content: $content"
        if ($content -match "https://[a-zA-Z0-9-]+\.loca\.lt") {
            $tunnelUrl = $Matches[0]
            break
        }
    }
}

if ($tunnelUrl) {
    Write-Host "Localtunnel successfully started at: $tunnelUrl"
} else {
    Write-Host "Failed to get tunnel URL. Please check the log file: $logFile"
}
