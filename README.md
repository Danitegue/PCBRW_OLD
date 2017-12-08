# PCBasic_Brewer_Repo
A repository with all the needed things to run and control BREWER instruments software, under a Pyhton enviroment.

Based in the https://github.com/robhagemans/pcbasic/ code.

## Contents
* **brw#185:** 
Folder of the Brewer program, with all the necessary files to make it run. This includes the main BASIC program "main.asc", routines, schedules, calibration files, etc. The program can be used in both, online and offline mode, having or not a real brewer connected to the serial port. 

* **pcbasic_brewer:** 
PC-BASIC interpreter of robhagermans, specifically customized to handle serial communications with Brewers)

* **BrewerSimulator.py:**
A program used to simulate the brewer serial port answers, through a virtual com port brigde (com2com software), in order to debug the serial communications in onlne mode, without the need of having a real brewer instrument connected to the pc.

* **.idea:**
This folder is an already configured pycharm project, with all the launchers needed to run pcbasic with a pygame interface, and to run the main.asc brewer program with line per line debbugging capabilities. To use it is only needed to run pycharm > Open > Select the containing folder C:\PCBasic_Brewer_Repo, and it automatically will detect the existing project.



## Installation
* Create a new folder into unit C. This repo is already configured to work in a folder called C:\PCBasic_Brewer_Repo\
* Clone this repository into that folder. 
* Install python 2.7. (Or Anaconda package with python 2.7) 
* Install the needed extra libraries: pip install pypiwin32 pysdl2 numpy pygame pyaudio (pyserial won't be needed since this customized version of pcbasic_brewer has an in built customized version of pyserial)



## Test PCBASIC
* run the program C:\PCBasic_Brewer_Repo\Launcher_pcbasic.bat
a console windows will open showing the pcbasic enviroment:
![pcbasic_test_image](https://www.dropbox.com/s/excytyvxuscajlt/PCBASIC_test.PNG?dl=0)



