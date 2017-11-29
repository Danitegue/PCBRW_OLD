@echo off
rem  Use this batch file to run the Brewer software without a Brewer
rem  connected.  DO NOT USE with Brewer connected since motors may
rem  move improperly.

rem ****************************************************************************
rem Use the variables in this section to configure the execution of the program
rem ****************************************************************************
rem Use NOBREW=1 if the brewer is not connected
set NOBREW=
rem Set the BREWDIR environment variable to the proper directory (full path)
set BREWDIR=c:\
rem BREWER_MAIN indicates the folder in which the main GW-Basic file is contained
set BREWER_MAIN=C:\GWBasic_Interpreter\brw#185\Program
rem BREWER_DEVICE indicates the folder in which the data related to the specific brewer being connected is included
set BREWER_DEVICE=C:\GWBasic_Interpreter\brw#185\bdata185
rem MAIN_FILE is the name of the main GW-Basic file
set MAIN_FILE=main.asc
rem COM_PORT is the identifier of the port in which the brewer is connected
set COM_PORT=COM14
rem PCBASIC_PATH is the path in which the PC-BASIC is located
set PCBASIC_PATH=C:\GWBasic_Interpreter\pcbasic_nestor
rem PYTHON_DIR is the folder in which the python.exe is located
set PYTHON_DIR=C:\Users\pandora\Anaconda2
rem ADDITIONAL_OPTIONS set other options that are desired to be used (for example, ADDITIONAL_OPTIONS="-f=10 --debug")
set ADDITIONAL_OPTIONS="-f=10 --max-memory=67108864 --logfile=C:\O_nestor.txt"


rem ****************************************************************************
rem Do not change anything below this line
rem ****************************************************************************
@echo on

REM set PATH=%PATH%;C:\Program Files (x86)\PC-BASIC

rem * Change the prompt as a reminder that the Brewer software is running
PROMPT Brewer $P$G
rem * Change to the Brewer directory to ensure correct operation (full path)
set CURR_DIR=%CD%
cd %BREWER_MAIN%



rem * Run the Brewer software
%PCBASIC_PATH%\ansipipe-launcher.exe %PYTHON_DIR%\python.exe %PCBASIC_PATH%\pcbasic.py "--run=%MAIN_FILE%" "--mount=C:%BREWER_MAIN%,D:%BREWER_DEVICE%" "--com1=PORT:%COM_PORT%" "--interface=ansi" "-f=10" "--max-memory=67108864" "--quit=False" "--double=True" "-s=512" "--use-serial-brewer=True" "--logfile=C:\O_nestor.txt"  

rem * Undo what was done above
PROMPT $P$G
set BREWDIR=
set NOBREW=
cd /D %CURR_DIR%

ECHO "Have a nice day!"