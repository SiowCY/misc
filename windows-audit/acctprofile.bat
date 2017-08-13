@echo off
setlocal enabledelayedexpansion

echo ^<?xml version="1.0"?^> 
echo. 
REM IP Address of the current machine
if exist ip.txt del ip.txt 
ipconfig | find "IPv4" > ip.txt
for /F "delims=: tokens=2 USEBACKQ" %%p in (`type ip.txt ^| find "IPv4"`) do (set ip=%%p)
echo ^<ipaddr ipaddr="%ip%"^> 
echo. 
del ip.txt

REM Show hostname
for /F "tokens=1 USEBACKQ" %%h IN (`hostname`) DO ( set hn=%%h )
echo ^<hostname hostname="%hn%"^> 
echo. 

REM OS Name
if exist osname.txt del osname.txt
systeminfo | find "OS Name" > osname.txt
for /F "tokens=3*" %%a in (osname.txt) do (set osn=%%a %%b)
echo ^<osname osname="%osn%"^> 
echo. 
del osname.txt

REM OS Version
if exist osversion.txt del osversion.txt
systeminfo | find "OS Version" > osversion.txt
type osversion.txt | find "Build" > osversion2.txt
for /F "tokens=3* delims= " %%a in (osversion2.txt) do (set osv=%%a %%b)
echo ^<osversion osversion="%osv%"^> 
echo. 
del osversion.txt
del osversion2.txt

REM Users Password Policy
net user | findstr /V "command" | findstr /V "\-\-\-" | findstr /V "accounts" > localuser.txt
for /F "tokens=1* delims= " %%a in (localuser.txt) do (
	echo %%a >> userlist.txt
	echo %%b >> userlist.txt
	
	)
	
echo > user.txt
for /F "tokens=1* delims= " %%a in (userlist.txt) do (
	echo %%a >> user.txt
	echo %%b >> user.txt
	)
	
type user.txt | findstr /v "ECHO" | findstr /x /v "is" | findstr /x /v "off" | find /V "is off." > useronly.txt
for /F "tokens=1 delims= " %%a in (useronly.txt) do (

	REM Each user has own X-policy.txt
	net user %%a >> %%a-policy.txt

	echo ^<user username="%%a"^> 
	echo.
	
	REM Account Activation
	echo ^<account_activation^> 
	type %%a-policy.txt | findstr "active" > %%a-active.txt
	for /F "tokens=3 delims= " %%h in (%%a-active.txt) do (
	 	echo %%h 
	 	)
	echo ^</account_activation^> 
	
	REM Account Creation
	echo ^<account_creation^> 
	dir /T:C /A:D "C:\Users" | find "%%a" > %%a-create.txt
	for /F "tokens=1 delims= " %%i in (%%a-create.txt) do (
	 	echo %%i 
	 	)
	echo ^</account_creation^> 
	
	REM Account Last Logon
	echo ^<account_lastlog^> 
	type %%a-policy.txt | find "Last logon" > %%a-lastlog.txt
	for /F "tokens=3 delims= " %%h in (%%a-lastlog.txt) do (
	 	echo %%h 
	 	)
	echo ^</account_lastlog^> 
	
	REM Password Last Changed
	echo ^<password_lastchg^> 
	type %%a-policy.txt | find "last set" > %%a-lastchg.txt
	for /F "tokens=4 delims= " %%h in (%%a-lastchg.txt) do (
	 	echo %%h 
	 	)
	echo ^</password_lastchg^> 
	
	REM Password never expires
	echo ^<password_expires^> 
	type %%a-policy.txt | find "Password expires" > %%a-pexpires.txt
	for /F "tokens=3 delims= " %%h in (%%a-pexpires.txt) do (
	 	echo %%h 
	 	)
	echo ^</password_expires^> 

	REM Account never expires
	echo ^<account_expires^> 
	type %%a-policy.txt | find "Account expires" > %%a-aexpires.txt
	for /F "tokens=3 delims= " %%h in (%%a-aexpires.txt) do (
	 	echo %%h 
	 	)
	echo ^</account_expires^> 
	
	REM Local group checking
	REM Extract the Local Group and Group Group to one file
	type %%a-policy.txt | C:\grouprepl.bat ".*M    " "" | C:\groupfindrepl.bat "Local Group" /e:"The command completed" /o:0:-1 > %%a-group.txt
	
	echo ^<local_group^> 
	echo > %%a-group2.txt
	for /F "tokens=1* delims=*" %%m in (%%a-group.txt) do (
		echo %%m >> %%a-group2.txt
		echo %%n >> %%a-group2.txt
		)
	
	type %%a-group2.txt | findstr /v "ECHO" | findstr /x /v "is" | findstr /x /v "off" | find /V "is off." | find /V "Local Group Memberships" | find /V "Global Group memberships" | find /V "None" > %%a-group3.txt

	echo > %%a-group4.txt
	for /F "tokens=1* delims= " %%o in (%%a-group3.txt) do (
		echo %%o >> %%a-group4.txt
		echo %%p >> %%a-group4.txt
		)
	
	type %%a-group4.txt | findstr /v "ECHO" | findstr /x /v "is" | findstr /x /v "off" | find /V "is off." | find /V "Echo is off." > %%a-group5.txt
	
	echo > %%a-group6.txt
	for /F "tokens=1* delims=*" %%q in (%%a-group5.txt) do (
	 	echo %%q >> %%a-group6.txt
		echo %%r >> %%a-group6.txt
	 	)
	type %%a-group6.txt | findstr /v "ECHO" | findstr /x /v "is" | findstr /x /v "off" | find /V "is off." | find /V "Echo is off." > %%a-grouponly.txt
	type %%a-grouponly.txt
	echo ^</local_group^>
	
	REM Task scheduler by the user
	schtasks /query /v /fo list > schtask1.list

	type schtask1.list | findstr /c:"TaskName" /c:"Run As User" > schtask2.list

	echo > schtask3.list
	for /f "tokens=2 delims=:" %%h in (schtask2.list) do (
		echo %%h >> schtask3.list
		)
	echo > schtask4.list
	for /f "tokens=* delims= " %%h in (schtask3.list) do (
		echo %%h >> schtask4.list
		)
	type schtask4.list | find /v "ECHO" | find /v "ECHO is off." > schtask5.list
	
	echo > schtask6.list
	set "line="
	
	(for /f "usebackq tokens=*" %%g in (schtask5.list) do (
		if defined line (
			echo !line!,%%g
			set "line="
		) else (
			set "line=%%g"
		)
	)) > schtask6.list
	
	type schtask6.list | find /v "SYSTEM" | find /v "NETWORK SERVICE" | find /v "LOCAL SERVICE" | find /v "INTERACTIVE" > schtask7.list
	rem set "schuser=%%a"
	echo ^<usertask^>
	
	for /f "tokens=1* delims=," %%u in ('type schtask7.list ^| find /i "%%a"') do (
	 	if [%%u] NEQ [] ( 
			echo %%u
			) else (
			echo None
			)
		
		)
	echo ^</usertask^>
	REM No requirement to check whether the user is in domain, when use "net user" it is showing the local users.
	
	
	echo ^</user^> 
	
	rem del schtask7.list
	rem del schtask6.list
	rem del schtask5.list
	rem del schtask4.list
	rem del schtask3.list
	rem del schtask2.list
	rem del schtask1.list
	del %%a-grouponly.txt
	del %%a-group4.txt
	del %%a-group3.txt
	del %%a-group2.txt
	del %%a-group.txt
	del %%a-aexpires.txt
	del %%a-pexpires.txt
	del %%a-lastchg.txt
	del %%a-lastlog.txt
	del %%a-create.txt
	del %%a-active.txt
	del %%a-policy.txt
	)
	
	
del localuser.txt
del userlist.txt
del user.txt
rem del useronly.txt

echo ^</osversion^> 
echo ^</osname^> 
echo ^</hostname^> 
echo ^</ipaddr^> 
goto:eof






