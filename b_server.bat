call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat"
pushd E:\projects\server\fy\build

msbuild server.sln /m:4
rem msbuild server.sln /m:4 /t:Rebuild

echo done!
pause