@echo off
rem  Use this batch file to run the Brewer software.  To run
rem  it as part of your AUTOEXEC.BAT, add the following line
rem  to the end of the AUTOEXEC.BAT file:
rem
rem     call brewer.bat
rem
rem  (Make sure that BREWER.BAT is somewhere on your path!)

rem *
rem * Change to the Brewer directory to ensure correct operation (full path)
rem *
cd c:\BREWER.163\brewer

rem *
rem * Set the BREWDIR environment variable to the proper directory (full path)
rem *
set NOBREW=
set BREWDIR=C:\BREWER.163\brewer
rem *
rem * Change the prompt as a reminder that the Brewer software is running
rem *
PROMPT Brewer $P$G

rem *
rem * Run the Brewer software
rem *
gwbasic main /f:10

rem *
rem * Undo what was done above
rem *
PROMPT $P$G
set NOBREW=
set BREWDIR=
