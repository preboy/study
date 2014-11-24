@echo off

set path="C:\Program Files\MySQL\MySQL Server 5.6\bin";%path%;

echo sync dev_world_____________________
mysqldump.exe --set-gtid-purged=off -h172.31.251.130 -udev -pdev -d dev_world > dev_world.sql
mysql -h127.0.0.1 -udev -pdev dev_world < dev_world.sql

echo sync dev_uname_____________________
mysqldump.exe --set-gtid-purged=off -h172.31.251.130 -udev -pdev -d dev_uname > dev_uname.sql
mysql -h127.0.0.1 -udev -pdev dev_uname < dev_uname.sql

echo sync dev_log_____________________
mysqldump.exe --set-gtid-purged=off -h172.31.251.130 -udev -pdev -d dev_log > dev_log.sql
mysql -h127.0.0.1 -udev -pdev dev_log < dev_log.sql

echo export account ....
mysqldump.exe --set-gtid-purged=off -h172.31.251.130 -udev -pdev dev_log auth> auth.sql
mysql -h127.0.0.1 -udev -pdev dev_log < auth.sql

del dev_world.sql
del dev_uname.sql
del dev_log.sql
del auth.sql

echo done! 
pause
