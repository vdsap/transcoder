[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function pressEnterToExit {
    Write-Host "Press Enter to exit... " -NoNewline
    [void][System.Console]::ReadLine()
}

$executablePath = Join-Path (pwd).Path Transcoder.exe

reg add "HKCU\Software\Classes\SystemFileAssociations\.mp4\shell\Transcoder" /ve /d "Transcoder" /f > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

reg add "HKCU\Software\Classes\SystemFileAssociations\.mp4\shell\Transcoder" /v "Icon" /d "$executablePath,0" /f > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

$command = "`"$executablePath`" `"%1`""
reg add "HKCU\Software\Classes\SystemFileAssociations\.mp4\shell\Transcoder\command" /ve /d "$command" /f  > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

reg add "HKCU\Software\Classes\SystemFileAssociations\.mkv\shell\Transcoder" /ve /d "Transcoder" /f > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

reg add "HKCU\Software\Classes\SystemFileAssociations\.mkv\shell\Transcoder" /v "Icon" /d "$executablePath,0" /f > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

$command = "`"$executablePath`" `"%1`""
reg add "HKCU\Software\Classes\SystemFileAssociations\.mkv\shell\Transcoder\command" /ve /d "$command" /f  > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

reg add "HKCU\Software\Classes\Folder\shell\Transcoder_folder" /ve /d "Transcoder" /f > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

reg add "HKCU\Software\Classes\Folder\shell\Transcoder_folder" /v "Icon" /d "$executablePath,0" /f > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

reg add "HKCU\Software\Classes\Folder\shell\Transcoder_folder\command" /ve /d "$command" /f > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ reg error"
    pressEnterToExit
    exit $LASTEXITCODE
}

Write-Host "✅ reg values added"
pressEnterToExit
