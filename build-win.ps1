echo "Creating executable"

try {C:/Python39/Scripts/pyinstaller rss-tube.spec}
catch {pyinstaller rss-tube.spec}

echo "Creating installer"
iscc rss-tube.iss
