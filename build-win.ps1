echo "Creating executable"

try {C:/Python39/Scripts/pyinstaller rss-tube.spec}
catch {pyinstaller rss-tube.spec}

$compress = @{
  Path = "dist\rsstube"
  CompressionLevel = "Optimal"
  DestinationPath = "rsstube-portable-win.zip"
}
Compress-Archive @compress

echo "Creating installer"
iscc rss-tube.iss
