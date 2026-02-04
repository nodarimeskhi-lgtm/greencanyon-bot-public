$ids = @(
"140eLYyWHgMpdTd6R3BYx3W_dtHSHZBXP",
"142vCL0VA18mSheuUdSZElVcJs_YUoG0M",
"16XBYEDAXFOngrLUXwyyhuoG0VuvFjBps",
"18w3-AobceUOsqi9O88W5HXrv_dGBEOtP",
"18xm2QkSZJ34NUItYOXBfwTCUCCAEgCd6",
"1LifCJCvsc6WzKBpu_W8yrLLMfMQ6Jwn6",
"1OXxUT-5Bp3bplZtZpuWvEPn34J1QH_bd",
"1QGHQbmuKVTWLVN974C_OHG-cAmzznUrZ",
"1QhoGwF3T89gOIPhL8HFFjsv_cQHf3OV_",
"1UmBwEsIji-uvoijHJsC7TiP4KtL9D_-0",
"1XNaPH1CqvJpiU1DzeIYE2RtObPAUrL3I",
"1hPaTVp5Q6_JudomB-8WZmbh1fR6z_xyR"
)

$i = 2
foreach ($id in $ids) {
    Write-Host "Downloading $id to image_$i.dat..."
    curl.exe -L "https://drive.google.com/uc?export=download&id=$id" -o "Marketing/Assets/image_$i.dat"
    $i++
}
mv "Marketing/Assets/file_1.dat" "Marketing/Assets/image_1.dat"
Write-Host "Download Complete"
