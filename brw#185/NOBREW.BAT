@echo off
rem  Use this batch file to run the Brewer software without a Brewer
rem  connected.  DO NOT USE with Brewer connected since motors may
rem  move improperly.

rem *
rem * Change to the Brewer directory to ensure correct operation (full path)
rem *
C:
cd \Brw#185\Program
rem *
rem * Set the BREWDIR environment variable to the proper directory (full path)
rem *
set NOBREW=1
set BREWDIR=c:\Brw#185\Program
setdate
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
set BREWDIR=
set NOBREW=
