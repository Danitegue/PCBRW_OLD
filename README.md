# PCBasic_Brewer_Repo
A repository with all the needed things to run and control BREWER instruments software, under a Pyhton enviroment.
(Not finished yet!!)

Based in the Rob Hagemans PCBasic project: https://github.com/robhagemans/pcbasic/ 

## Contents
* **brw#185:** 
Folder of the Brewer program, with all the necessary files to make it run. This includes the main BASIC program "main.asc", routines, schedules, calibration files, etc. The program can be used in both, online and offline mode, having or not a real brewer connected to the serial port. The program needs two enviroment variables set to be able to run NOBREW, and BREWDIR, both are set in the launchers.

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
![pcbasic_test_image](https://www.dropbox.com/s/excytyvxuscajlt/PCBASIC_test.PNG?dl=0)


## Configurations needed for running the Brewer Software with PCBASIC:
* for running the brewer program is needed to configure the PCBASIC.INI file, which for windows is created after the first launch at 
C:\Users\[username]\AppData\Roaming\pcbasic-dev\PCBASIC.INI, with the following entries:
  * debug=True
  * scaling=native
  
* Also is needed to create a 'C:\Temp' folder, in which is going to be saved the pcbasic session output file (pcbasic_brewer_log.txt, very useful for debugging). 


## Run the Brewer software, offline mode, into an ansi console:
* run the launcher C:\PCBasic_Brewer_Repo\pcbasic_brewer\Launcher_brewer185_nobrew.bat, 
a console window will open showing the main.asc brewer program:
![pcbasic_test_image](https://www.dropbox.com/s/zgpu4teoumq0vni/Test_mainasc_ansi_nobrew.PNG?dl=0)


## Prepare pycharm:
For being able to run pcbasic programs from pycharm with line per line debbuging capabilities is needed to configure pycharm:
* Open pycharm
* Go to File > Open > Select the repo folder C:\PCBasic_Brewer_Repo, and it automatically will detect the existing project into the .idea folder. Open the project.
* Prepare the debugging configurations: go to Run > Edit Configurations... here is needed to adapt the paths of the script, installed python interpreter, and working directory for each configuration, with the correct paths in your PC.
![pcbasic_test_image](https://www.dropbox.com/s/8deo02hejv6040k/Pycharm2.PNG?dl=0)


## Test the Brewer software, offline mode, using pycharm, into a pygame console:
* In the configuration selector of pycharm, select brewer185_pygame_nobrew, then run or debug the configuration as prefered.
![pcbasic_test_image](https://www.dropbox.com/s/ywqtw8s87srrkq2/Pycharm3.PNG?dl=0)


## Test to run some routines into the brewer program:
Once the brewer program is loaded in offline mode, one can try to run some offline-compatible routines to test the proper function of the software. For example just writting pdhp and pressing enter, the program will execute the routine pd and then the routine hp.

## To do:
-Some string variables are being detached. Researching the causes... https://github.com/robhagemans/pcbasic/issues/49)




