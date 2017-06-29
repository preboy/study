
@echo off

setlocal

set PATH="C:\Program Files\Beyond Compare 4";%PATH%

if "%1"=="" (
    echo need at least 1 param
    goto End
)

if not exist %1 (
    echo src file not exist
    goto End
)

set src=%1
rem echo %src%

set dst1=%src:~3,11%
set dst2=%src:~3,8%
rem echo %dst1%
rem echo %dst2%

if %dst1%==projects_yy    goto Do_yy
if %dst2%==projects       goto Do_Master
goto End


:Do_yy
    set tmp1=%src:projects_yy=projects%
    bcomp %tmp1% %src%
    goto End


:Do_Master
    set tmp1=%src:projects=projects_yy%
    bcomp %src% %tmp1%
    goto End


:End
    endlocal
    echo The End!!!
