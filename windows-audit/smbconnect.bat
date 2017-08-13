@echo off
setlocal enabledelayedexpansion
set ip=%1
set username=%2
set password=%3
set adminpass=%4
call:checkarguments
call:smbconnect

goto end

:checkarguments
if "%ip%"=="" goto usage
if "%username%"=="" goto usage
if "%password%"=="" goto usage
goto:eof

:usage
@echo Require Administrator Account
@echo Usage  : smbconnect.bat ^<IP^> ^<username^> ^<password^> 
@echo Example: smbconnect.bat 192.168.10.2 Administrator P^5svV0rb
exit /b 0
goto end
goto:eof


:smbconnect
echo net use g: \\%ip%\C$ /user:%username% %password% /p:yes

REM Create SMB with G drive
net use g: \\%ip%\C$ /user:%username% %password% /p:yes

REM COPY the bat file to the G drive
copy C:\Users\user\Desktop\acctprofile.bat G:\
copy C:\Users\user\Desktop\grouprepl.bat G:\
copy C:\Users\user\Desktop\groupfindrepl.bat G:\

REM psexec run the bath file
psexec -u %username% -p %password% \\%ip% "C:\acctprofile.bat" > %ip%-acctprofile.xml
psexec -u %username% -p %password% \\%ip% -s -d cmd.exe /c "del C:\acctprofile.bat"
psexec -u %username% -p %password% \\%ip% -s -d cmd.exe /c "del C:\grouprepl.bat"
psexec -u %username% -p %password% \\%ip% -s -d cmd.exe /c "del C:\groupfindrepl.bat"

REM Delete net use g:
net use g: /delete
goto:eof



:end
echo.
echo. END
exit /b 2
GOTO:eof
