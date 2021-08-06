echo "Creating executable"

try {C:/Python38/Scripts/pyinstaller rss-tube.spec}
catch {pyinstaller rss-tube.spec}

try {Remove-Item "dist/rsstube/d3dcompiler_47.dll"} catch {}
try {Remove-Item "dist/rsstube/opengl32sw.dll"} catch {}
try {Remove-Item "dist/rsstube/Qt5Quick.dll"} catch {}
try {Remove-Item "dist/rsstube/Qt5Qml.dll"} catch {}
try {Remove-Item "dist/rsstube/libGLESv2.dll"} catch {}
try {Remove-Item "dist/rsstube/Qt5Network.dll"} catch {}
try {Remove-Item "dist/rsstube/Qt5QmlModels.dll"} catch {}
try {Remove-Item "dist/rsstube/Qt5Svg.dll"} catch {}
try {Remove-Item "dist/rsstube/Qt5WebSockets.dll"} catch {}

echo "Creating installer"
iscc rss-tube.iss
Move-Item "inno-output\rss-tube-setup.exe" "rsstube-installer-win.exe"
