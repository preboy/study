
@echo off


if "%1"=="" (
    echo need at least 1 param
    goto End
)

if not exist %1 (
    echo src file not exist
    goto End
)

set src=%1
echo %src%

set dst1=%src:~3,11%
set dst2=%src:~3,8%


rem     echo %dst1%
rem     echo %dst2%

if %dst1%==projects_yy    goto Do_yy
if %dst2%==projects       goto Do_Master
goto End


:Do_yy
    set tmp=%src:projects_yy=projects%
    rem echo %tmp%
    ep %tmp%
    goto End


:Do_Master
    set tmp=%src:projects=projects_yy%
    rem echo %tmp%
    ep %tmp%
    goto End


:End
   echo The End!!!
   exit 1
