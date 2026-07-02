# Powershell Script to run OCR on extracted PDF pages

[void][Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
[void][Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
[void][Windows.Media.Ocr.OcrEngine, Windows.Media.Ocr, ContentType = WindowsRuntime]

$imageDir = "c:\Users\Nodar\2026 antigraviti\scratch\pdf_pages"
$outFile = "c:\Users\Nodar\2026 antigraviti\scratch\ocr_letters_output.txt"
$results = @()

$ka_lang = New-Object Windows.Globalization.Language("ka")
$isKaSupported = [Windows.Media.Ocr.OcrEngine]::IsLanguageSupported($ka_lang)
$results += "Georgian language OCR supported: " + $isKaSupported

if ($isKaSupported) {
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($ka_lang)
} else {
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
}

$results += "Engine Language: " + $engine.RecognizerLanguage.LanguageTag

for ($i = 1; $i -le 5; $i++) {
    $imgName = "page_" + $i + ".png"
    $imgPath = Join-Path $imageDir $imgName
    if (Test-Path $imgPath) {
        $results += "`n================ PAGE " + $i + " ================"
        try {
            $file = [Windows.Storage.StorageFile]::GetFileFromPathAsync($imgPath).GetResults()
            $stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetResults()
            $decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetResults()
            $bitmap = $decoder.GetSoftwareBitmapAsync().GetResults()
            $ocrResult = $engine.RecognizeAsync($bitmap).GetResults()
            $results += $ocrResult.Text
        } catch {
            $errMsg = $_.ToString()
            $results += "Error processing page " + $i + ": " + $errMsg
        }
    }
}

$results | Out-File -FilePath $outFile -Encoding utf8
Write-Host "OCR Completed successfully"
