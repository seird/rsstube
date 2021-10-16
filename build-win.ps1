echo "Creating executable"

try {C:/Python39/Scripts/pyinstaller rss-tube.spec}
catch {pyinstaller rss-tube.spec}

try {Remove-Item "dist/rsstube/d3dcompiler_47.dll"} catch {}
try {Remove-Item "dist/rsstube/opengl32sw.dll"} catch {}
try {Remove-Item "dist/rsstube/libGLESv2.dll"} catch {}

echo "Creating installer"
iscc rss-tube.iss
