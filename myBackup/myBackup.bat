cls
prompt
PATH=%PATH%;C:\myPro\myBackup

SET "WORK_DIR=C:\myPro\myBackup"
SET "BACK_DIR=D:\zz.Backup"
SET "LOG_FILE=%WORK_DIR%\myBackup.log"
SET "BACKUP_LIST=%WORK_DIR%\myBackup_list.txt"

if exist %LOG_FILE% (
    echo %LOG_FILE% file exists. So logs are appended to .bak file. >> %LOG_FILE%
    type %LOG_FILE% >> %LOG_FILE%.bak
    ) else (
      type NUL > %LOG_FILE%
    )
	
if exist %BACK_DIR% (
    echo %BACK_DIR% file exists. >> %LOG_FILE%
	) else (
        	mkdir "%BACK_DIR%"
			echo %BACK_DIR% created. >> %LOG_FILE%
	)
 
   
echo "======================================================================================================" >> %LOG_FILE%
echo If you want to see logs at realtime, use "Get-Content %WORK_DIR%\myBackup.log -Wait" in powershell mode >> %LOG_FILE%
echo %date%_%time%  Begining myBackup.bat >> %LOG_FILE%
cd %WORK_DIR%
python myBackup_01.py "%BACKUP_LIST%" "%BACK_DIR%"
echo %date%_%time%  Ended myBackup.bat >> %LOG_FILE%
echo "======================================================================================================" >> %LOG_FILE%