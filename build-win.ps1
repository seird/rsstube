echo "Creating executable"

try {C:/Python39/Scripts/pyinstaller rss-tube.spec}
catch {pyinstaller rss-tube.spec}

try {Remove-Item "dist/rsstube/opengl32sw.dll"} catch {}

echo "Creating installer"
iscc rss-tube.iss
