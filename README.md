# PCBasic_Brewer_Repo
A repository with all the needed things to run and control BREWER instruments software, under a Pyhton enviroment.
(Not finished yet!!)

Based in the Rob Hagemans PCBasic project: https://github.com/robhagemans/pcbasic/ 

Main programmers: Daniel Santana Díaz, Nestor Morales Hernández.

Principal collaborators: Alberto Redondas Marrero, Sergio Leon Luis, Virgilio Carreño.

## Contents
* **brw#185:** 
Folder of the Brewer program, with all the necessary files to make it run. This includes the main BASIC program "main.asc", routines, schedules, calibration files, etc. The program can be used in both, online and offline mode, having or not a real brewer connected to the serial port. The program needs two enviroment variables set for being able to run: NOBREW, and BREWDIR. (both are set in the launchers.)

* **pcbasic_brewer:** 
PC-BASIC interpreter of robhagermans, specifically customized to handle serial communications with Brewers, and to ignore the extra arguments added by pycharm when debugging.

* **BrewerSimulator.py:**
A program used to simulate the brewer instrument serial port answers, through a virtual com port brigde (com2com software), in order to debug the serial communications in onlne mode, without the need of having a real brewer instrument connected to the pc.

* **.idea:**
This folder is an already configured pycharm project, with all the launchers needed to run pcbasic or the main.asc program into a pygame interface, with line per line debbugging capabilities.



## Installation:
* Create a new folder into unit C. This repo is already configured to work in a folder called C:\PCBasic_Brewer_Repo\
* Clone this repository into that folder. 
* Install python 2.7. (Or Anaconda package with python 2.7) 
* Install the needed extra libraries: pip install pypiwin32 pysdl2 numpy pygame pyaudio (pyserial won't be needed since this customized version of pcbasic_brewer has an in built customized version of pyserial)


## Run the PCBASIC interpreter into an ansi console:
* run the launcher C:\PCBasic_Brewer_Repo\pcbasic_brewer\Launcher_pcbasic.bat, a console window will open showing the pcbasic enviroment:

![pcbasic_test](images/PCBASIC_test_preview.png)


## Configurations needed for running the Brewer Software with PCBASIC: 
* In the provided launchers it is defined to write a log file of the pcbasic session (pcbasic_brewer_log.txt) into 'C:\Temp' folder. So it is needed to create this folder or modify the launchers accordingly. 

* Only in the case of needing an extended debugging file (for COM communications, or memory debug) it is useful to configure the PCBASIC.INI file, which for windows is created after the first launch at 
C:\Users\[username]\AppData\Roaming\pcbasic-dev\PCBASIC.INI, uncommenting the following entries:
  * debug=True
  
  Other options for extended debugging are:
  * To enable the memory addressing messages into the log file: In file \pcbasic_brewer\pcbasic\basic\strings.py; set StringsLogging=True
  * To enable the COM port communication messages into the log file: In file \pcbasic_brewer\pcbasic\basic\devices\ports.py; set self.log_COM_Messages=True
  * To enable the COM port event messages into the log file: In file \pcbasic_brewer\pcbasic\basic\events.py; set self.log_COM_events = True


## Run the Brewer software, offline mode, into an ansi console:
* run the launcher C:\PCBasic_Brewer_Repo\pcbasic_brewer\Launcher_brewer185_nobrew.bat, 
a console window will open showing the main.asc brewer program:

![Test_mainasc_ansi_nobrew](images/Test_mainasc_ansi_nobrew.PNG)

## Test to run some routines into the brewer program:
Once the brewer program is loaded in offline mode, one can try to run some instrument offline-compatible routines to test the proper function of the software. For example just writting pdhp and pressing enter, the program will execute the routine pd and then the routine hp.

![OfflineTest1](images/OfflineTest1.PNG)
![OfflineTest2](images/OfflineTest2.PNG)
![OfflineTest3](images/OfflineTest3.PNG)

## Run the Brewer software, online mode, into an ansi console:
This allows to control a real instrument connected to the pc.
* Configure the COM port number in the launcher C:\PCBasic_Brewer_Repo\pcbasic_brewer\Launcher_brewer185.bat
* run the launcher.

a console window will open showing the main.asc brewer program, in the same way of the previous images, but with the com port communications enabled, and being able to control a real instrument through the configured com port. 

![OfflineTest1](images/OfflineTest1.PNG)
![OnlineTest01](images/OnlineTest01.PNG)
![OnlineTest1](images/OnlineTest1.PNG)



-----------------------------------------------------------------------------------------------
## Brewer Simulator:
This is a small script that simulates the instrument com port answers when connecting, and also the answers for a few brewer routines like hp or hg (only these ones for now). It is used for debugging the pcbasic com port communications, without the need of having a real instrument connected to the pc.

For using it, it is needed install a com bridge in the pc (in windows can be used the com0com software, for example), and also configure the Brewer launcher to use the com port number of the bridge.

One must run the BrewerSimulator.py script (cd C:\PCBasic_Brewer_Repo; python C:\PCBasic_Brewer_Repo\BrewerSimulator.py) before running the online Brewer Launcher (C:\PCBasic_Brewer_Repo\pcbasic_brewer\Launcher_brewer185.bat).

In the case of an installed COM14&COM15 bridge, and a Brewer launcher configured to use the COM14 the communications will be: 

* pcbasic <-> COM14 (Brewer software)
* COM14 <-> COM15 (COM Bridge)
* BrewerSimulator <-> COM15 (Instrument simulator)

![BrewerSimulator1](images/BrewerSimulator1.PNG)

----------------------------------------------------------------------------------

## For running or debugging pcbasic with pycharm:

### Prepare pycharm:
For being able to run pcbasic programs from pycharm with line per line debbuging capabilities is needed to configure pycharm:
* Open pycharm
* Go to File > Open > Select the repo folder C:\PCBasic_Brewer_Repo, and it automatically will detect the existing project into the .idea folder. Open the project.
* Prepare the debugging configurations: go to Run > Edit Configurations... here is needed to adapt the paths of the script, installed python interpreter, and working directory for each configuration, with the correct paths in your PC.

![Pycharm2](images/Pycharm2.PNG)

in the parameters section of the pycharm launcher one can configure the parameters to use in the pcbasic session:
![Pycharm2.1](images/Pycharm2.1.PNG)

in the enviroment variables one can configure the needed BREWDIR and NOBREW enviroment variables for using the brewer software:
![Pycharm2.2](images/Pycharm2.2.PNG)



### Test the Brewer software from pycharm, offline mode, into a sdl2 console:
* In the configuration selector of pycharm, select b185_pcbasic_brewer_sdl2_nobrew, then run or debug the configuration as prefered.

![Pycharm3](images/Pycharm3.PNG)







-------------------------------------------------------------

