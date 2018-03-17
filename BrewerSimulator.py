# -*- coding: utf-8 -*-
import time
import warnings
import serial
import io
from copy import deepcopy
import datetime
import logging


# This script is to simulate the COM port answers of a brewer instrument
# com0com software is needed to build a com14 to com15 bridge (for example).
# the main.asc brewer software has to connect to com14
# this program will be connected to the com15, answering the com14 questions.


#Parameters:
logfile="C:/Temp/BrewerSimulator_Log.txt"
comport='COM15'


#Brewer answers
brewer_none = ['\r','\n', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '->', '\x20', 'flush']

brewer_something = ['\r','\n', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\r','\n', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '->', '\x20', 'flush']

HPdict = {'M,9, 0;': 66347,
          'M,9, 10;': 96514,
          'M,9, 20;': 127847,
          'M,9, 30;': 159928,
          'M,9, 40;': 190187,
          'M,9, 50;': 215028,
          'M,9, 60;': 227272,
          'M,9, 70;': 230169,
          'M,9, 80;': 230486,
          'M,9, 90;': 231098,
          'M,9, 100;': 229171,
          'M,9, 110;': 217183,
          'M,9, 120;': 190595,
          'M,9, 130;': 159295,
          'M,9, 140;': 128684,
          'M,9, 150;': 97926,
          'M,9, 160;': 64454}

HGdict0 = {'HGdict':0,
          'O:M,10,50:M,9,50:R':451,
          'O:M,10,60:M,9,60:R':822,
          'O:M,10,70:M,9,70:R':2955,
          'O:M,10,80:M,9,80:R':16681,
          'O:M,10,90:M,9,90:R':35602,
          'O:M,10,100:M,9,100:R':52238,
          'O:M,10,110:M,9,110:R':70289,
          'O:M,10,120:M,9,120:R':90096,
          'O:M,10,130:M,9,130:R':109954,
          'O:M,10,140:M,9,140:R':121203,
          'O:M,10,150:M,9,150:R':123202,
          'O:M,10,160:M,9,160:R':117150,
          'O:M,10,170:M,9,170:R':98919,
          'O:M,10,180:M,9,180:R':80088,
          'O:M,10,190:M,9,190:R':59799,
          'O:M,10,200:M,9,200:R':40881,
          'O:M,10,210:M,9,210:R':21490,
          'O:M,10,220:M,9,220:R':4302,
          'O:M,10,230:M,9,230:R':587,
          'O:M,10,240:M,9,240:R':206}

HGdict1 = {'HGdict':1,
          'O:M,10,50:M,9,50:R':498,
          'O:M,10,60:M,9,60:R':889,
          'O:M,10,70:M,9,70:R':3226,
          'O:M,10,80:M,9,80:R':17812,
          'O:M,10,90:M,9,90:R':37250,
          'O:M,10,100:M,9,100:R':54635,
          'O:M,10,110:M,9,110:R':73008,
          'O:M,10,120:M,9,120:R':92826,
          'O:M,10,130:M,9,130:R':112827,
          'O:M,10,140:M,9,140:R':124267,
          'O:M,10,150:M,9,150:R':125312,
          'O:M,10,160:M,9,160:R':118875,
          'O:M,10,170:M,9,170:R':100355,
          'O:M,10,180:M,9,180:R':80903,
          'O:M,10,190:M,9,190:R':60590,
          'O:M,10,200:M,9,200:R':41175,
          'O:M,10,210:M,9,210:R':21619,
          'O:M,10,220:M,9,220:R':4190,
          'O:M,10,230:M,9,230:R':588,
          'O:M,10,240:M,9,240:R':218}

#Function to assign the each com port question with an answer
def check_line(line):

    gotkey=False
    answer=[]

    if '\n' == line and not gotkey:
        print 'Got keyword: \\n'
        answer=deepcopy(brewer_none)
        gotkey = True

    if '\r' == line and not gotkey:
        print 'Got keyword: \\r'
        answer=deepcopy(brewer_none)
        gotkey = True

    if 'F,0,2:V,' in line and not gotkey:
        print 'Got keyword: F,0,2:V,'
        answer = deepcopy(brewer_none)
        gotkey = True

    if '?MOTOR.CLASS[2]' in line and not gotkey:
        print 'Got keyword: ?MOTOR.CLASS[2]'
        #answer = ['TRACKERMOTOR']+deepcopy(brewer_something)+['wait0.5']+deepcopy(brewer_none)
        answer = ["\r"]+['TRACKERMOTOR'] + deepcopy(brewer_something)
        gotkey = True

    if 'B,0' in line and not gotkey:
        print 'Got keyword: B,0'
        answer=['wait0.5']+deepcopy(brewer_none)
        #answer = ['wait1'] + deepcopy(brewer_none)+['wait2'] + deepcopy(brewer_none)
        gotkey = True

    if 'B,1' in line and not gotkey:
        print 'Got keyword: B,1'
        answer=deepcopy(brewer_none)
        gotkey = True

    if 'B,2' in line and not gotkey:
        print 'Got keyword: B,2'
        answer=deepcopy(brewer_none)
        gotkey = True

    if '?TEMP[PMT]' in line and not gotkey:
        print 'Got keyworkd: ?TEMP[PMT]'
        answer=['19.158888']+deepcopy(brewer_something)
        gotkey = True

    if '?TEMP[FAN]' in line and not gotkey:
        print 'Got keyworkd: ?TEMP[FAN]'
        answer=['19.633333']+deepcopy(brewer_something)
        gotkey = True

    if '?TEMP[BASE]' in line and not gotkey:
        print 'Got keyworkd: ?TEMP[BASE]'
        answer=['17.637777']+deepcopy(brewer_something)
        gotkey = True

    if '?TEMP[EXTERNAL]' in line and not gotkey:
        print 'Got keyworkd: ?TEMP[EXTERNAL]'
        answer=['-37.777777']+deepcopy(brewer_something)
        gotkey = True

    if '?RH.SLOPE' in line and not gotkey:
        print 'Got keyworkd: ?RH.SLOPE'
        answer=['0.031088']+deepcopy(brewer_something)
        gotkey = True

    if '?RH.ORIGIN' in line and not gotkey:
        print 'Got keyworkd: ?RH.ORIGIN'
        answer=['0.863000']+deepcopy(brewer_something)
        gotkey = True

    if '?ANALOG.NOW[20]' in line and not gotkey:
        print 'Got keyworkd: ?ANALOG.NOW[20]'
        answer=['309']+deepcopy(brewer_something)
        gotkey = True

    if not gotkey:
        # 2 comma commands:
        if line.count(',')==2 and not gotkey:
            Mcmds = ['M,1,','M,2,','M,3,','M,4,','M,5,','M,9,','M,10,']
            for ii in range(len(Mcmds)):
                Mcm = Mcmds[ii]
                if Mcm in line and not gotkey:
                    print 'Got keyworkd: ',Mcm
                    answer=deepcopy(brewer_none)
                    gotkey = True
                    break

        # 3 comma commands:
        if line.count(',')==3 and not gotkey:
            Mcmds = ['R,0,7,1','R,1,1,1','R,0,0,4']
            for ii in range(len(Mcmds)):
                Mcm = Mcmds[ii]
                if Mcm in line and not gotkey:
                    print 'Got keyword: ',Mcm
                    answer=deepcopy(brewer_none)
                    gotkey = True
                    break

        # 4 comma commands:
        if line.count(',')==4 and not gotkey:
            # HG routine commands, like O:M,10,100:M,9,100:R
            for Dict in [HGdict0]:
                for ii in Dict.keys():
                    if ii in line and not gotkey:
                        print 'Got keyword: ', ii
                        answer = [str(Dict[ii])] + deepcopy(brewer_something)
                        gotkey = True
                        break
                if gotkey:
                    break

            # M,2, 12993:M,1, 208
            if not gotkey:
                if ('M,2,' in line) and ('M,1,' in line):
                    answer = deepcopy(brewer_none)
                    gotkey = True




        # 5 comma commands:
        if line.count(',')==5 and not gotkey:
            # HP routine commands, like M,9, 20;R, 6, 6,4;O
            for Dict in [HPdict]:
                for ii in Dict.keys():
                    if ii in line and not gotkey:
                        print 'Got keyword: ', ii
                        answer = [str(Dict[ii])] + deepcopy(brewer_something)
                        gotkey = True
                        break
                if gotkey:
                    break

    if not gotkey:
        if 'O' in line and line.count(',')==0:
            print 'Got keyworkd: O'
            answer = ["53,2,12,11,20431,11,11,22"]+deepcopy(brewer_something)
            gotkey = True

    if not gotkey:
        if 'T' in line and line.count(',') == 0:
            print 'Got keyworkd: T'
            answer = ["53,2,12,11,20431,11,11,22"]+deepcopy(brewer_something)
            gotkey = True

    if not gotkey:
        if '\x00'==line:
            print 'Got keyworkd: Null'
            answer = deepcopy(brewer_none)
            gotkey = True

    if not gotkey:
        print ""
        s= '!!!!! No key found for line:', str(line.replace('\r','\\r').replace('\n','\\n').replace('\x00','null'))
        print s
        logging.info(s)
        print ""
    return gotkey, answer



#Initialize the logger
logging.basicConfig(filename=logfile, format='%(asctime)s.%(msecs)04d %(message)s', level=logging.INFO, datefmt='%H:%M:%S', filemode='w')


#Open serial connection:
s='Opening '+comport+' serial connection...'
print s
logging.info(s)
sw = serial.Serial(comport, baudrate=1200, timeout=0.2)
sw.close()
sw.open()

#this is for changing the end of line detection
#sio = io.TextIOWrapper(io.BufferedRWPair(sw, sw))

time.sleep(1)
sw.flushInput()
line_counter=0

# when some of them are received in the initial connection with the brewer
s= 'Done. Monitoring serial...'
print s
logging.info(s)
with sw:
    while True:
        try:
            #line = sio.readline()
            line=''
            c= ''
            while c != '\r':
                c=sw.read(1)
                line +=c
            if not line:
                time.sleep(0.001)
                continue
            else:
                time.sleep(0.1)
                line_counter = line_counter + 1

                logl=str(line_counter)+" "+ str(datetime.datetime.now())+' Line received:'+ (str(line).replace('\r','\\r').replace('\n','\\n'))
                print logl
                logging.info('Line received:'+ (str(line).replace('\r','\\r').replace('\n','\\n')))
                gotkey, answer = check_line(line)

                if gotkey:
                    logl=str(datetime.datetime.now())+ ' - Writting to com port:'+ str(answer)
                    print logl
                    print ""
                    logging.info('Writting to COM port:'+ str(answer))
                    for a in answer:
                        if 'wait' in a:
                            time.sleep(float(a.split('wait')[1]))
                        elif 'flush' in a:
                            #sio.flush()
                            sw.flush()
                        else:
                            #sio.write(unicode(a))
                            sw.write(a)
        except ValueError:
            warnings.warn("Line {} didn't parse, skipping".format(line))
        except KeyboardInterrupt:
            sw.close()
            #ctrl+c
            print("Exiting")
            break