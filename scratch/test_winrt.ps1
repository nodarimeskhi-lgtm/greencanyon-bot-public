# Powershell script to test WinRT Async Await

function Await-WinRT ($operation) {
    # Load assembly
    Add-Type -AssemblyName "System.Runtime.WindowsRuntime"
    $task = [System.Runtime.InteropServices.WindowsRuntime.WindowsRuntimeSystemExtensions]::AsTask($operation)
    while (-not $task.IsCompleted) {
        Start-Sleep -Milliseconds 50
    }
    if ($task.Exception) {
        throw $task.Exception
    }
    return $task.Result
}

try {
    [void][Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
    $path = "c:\Users\Nodar\2026 antigraviti\scratch\pdf_pages\page_1.png"
    Write-Host "Getting file from path..."
    $op = [Windows.Storage.StorageFile]::GetFileFromPathAsync($path)
    $file = Await-WinRT $op
    Write-Host "File retrieved successfully: $($file.Name)"
} catch {
    Write-Host "Error: $_"
}
