@echo off

rem 	set path="C:\Program Files\MySQL\MySQL Server 5.6\bin";%path%;
rem    	set HOST=127.0.0.1


if "%1"=="" goto END1
if "%2"=="" goto END
if "%3"=="" goto END
if "%4"=="" goto END

set HOST=%1
set USER=%2
set PASS=%3
set PREF=%4

echo "Connect info...", %HOST% %USER% %PASS%

echo sync dev_world_____________________
mysql -h%HOST% -u%USER% -p%PASS%  %PREF%_world < E:\projects\server\fy\sql\fy_world.sql

echo sync dev_uname_____________________
mysql -h%HOST% -u%USER% -p%PASS%  %PREF%_uname < E:\projects\server\fy\sql\fy_uname.sql

echo sync dev_log_____________________
mysql -h%HOST% -u%USER% -p%PASS%  %PREF%_log   < E:\projects\server\fy\sql\fy_log.sql

goto END


:ERROR
	echo È±ÉÙ²ÎÊý
	goto :END

:END1
    echo end1

:END


echo done! 
pause

