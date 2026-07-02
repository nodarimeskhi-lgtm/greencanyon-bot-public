# Powershell script to print members of WinRT Async Operation

[void][Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$path = "c:\Users\Nodar\2026 antigraviti\scratch\pdf_pages\page_1.png"
$op = [Windows.Storage.StorageFile]::GetFileFromPathAsync($path)
$op | Get-Member | Out-File -FilePath "c:\Users\Nodar\2026 antigraviti\scratch\winrt_members.txt"
Write-Host "Members written"
