# -*- coding: utf-8 -*-
import time
import warnings
import serial
import io
from copy import deepcopy

# This script is to simulate the COM port answers of a brewer instrument
# com0com software is needed to build a com14 to com15 bridge.
# the main.asc brewer software has to connect to com14
# this program will be on com15, answering the com14 questions.

brewer_none = ['\n', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '->', '\x20', 'flush']

brewer_something = ['\n', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\n', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '->', '\x20', 'flush']


def check_line(line):
    gotkey=False
    answer=[]

    # if '\r' == line and not gotkey:
    #     print 'Got keyword: \\r'
    #     answer = ['->','\x20']
    #     gotkey = True

    if '\n' == line and not gotkey:
        print 'Got keyword: \\n'
        answer=deepcopy(brewer_none)
        #answer = ['->','\x20']
        gotkey = True

    #
    # if '\r\n' == line and not gotkey:
    #     print 'Got keyword: \\r \\n'
    #     answer=['->','\x20']
    #     gotkey=True
    #
    # if '\n\r' == line and not gotkey:
    #     print 'Got keyword: \\n \\r'
    #     answer=['->','\x20']
    #     gotkey=True

    if 'F,0,2:V,120,1' in line and not gotkey:
        print 'Got keyword: F,0,2:V,120,1'
        answer = deepcopy(brewer_none)
        gotkey = True

    if '?MOTOR.CLASS[2]' in line and not gotkey:
        print 'Got keyword: ?MOTOR.CLASS[2]'
        answer = ['TRACKERMOTOR']+deepcopy(brewer_something)
        gotkey = True

    if 'B,0' in line and not gotkey:
        print 'Got keyword: B,0'
        answer=['wait1']+deepcopy(brewer_none)
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
        if line.count(',')==2:
            Mcmds = ['M,1,','M,3,','M,4,','M,5,','M,9,','M,10,']
            for ii in range(len(Mcmds)):
                Mcm = Mcmds[ii]
                if Mcm in line and not gotkey:
                    print 'Got keyworkd: ',Mcm
                    answer=deepcopy(brewer_none)
                    gotkey = True

        if line.count(',')==5:
            Mcmds = ['M,9, 0','M,9, 10','M,9, 20','M,9, 30','M,9, 40','M,9, 50','M,9, 60','M,9, 70','M,9, 80','M,9, 90','M,9, 100','M,9, 110','M,9, 120','M,9, 130','M,9, 140','M,9, 150','M,9, 160']
            Mcmds_answs = ['90387', '120514', '152680', '183620', '210321', '225618', '229940', '230096', '230667','229401', '221551', '198234', '167614', '138376', '107594', '75888','43487']
            for ii in range(len(Mcmds)):
                Mcm = Mcmds[ii]
                Mcm_answ = Mcmds_answs[ii]
                if Mcm in line and not gotkey:
                    print 'Got keyword: ',Mcm
                    answer=[Mcm_answ]+deepcopy(brewer_something)
                    gotkey = True


        if line.count(',')==3:
            Mcmds = ['R,0,7,1','R,1,1,1','R,0,0,4']
            for ii in range(len(Mcmds)):
                Mcm = Mcmds[ii]
                if Mcm in line and not gotkey:
                    print 'Got keyword: ',Mcm
                    answer=deepcopy(brewer_none)
                    gotkey = True

        if line.count(',')==4:
            Mcmds = ['O:M,10,60:M,9,60:R','O:M,10,50:M,9,50:R','O:M,10,70:M,9,70:R','O:M,10,80:M,9,80:R','O:M,10,90:M,9,90:R','O:M,10,100:M,9,100:R','O:M,10,110:M,9,110:R','O:M,10,120:M,9,120:R','O:M,10,130:M,9,130:R','O:M,10,140:M,9,140:R','O:M,10,150:M,9,150:R','O:M,10,160:M,9,160:R','O:M,10,170:M,9,170:R','O:M,10,180:M,9,180:R','O:M,10,190:M,9,190:R','O:M,10,200:M,9,200:R','O:M,10,210:M,9,210:R','O:M,10,220:M,9,220:R','O:M,10,230:M,9,230:R','O:M,10,240:M,9,240:R']
            Mcmds_answs = ['389','300','375','594','1199','8746','19452','30016','40703','40500','30500','19000','8700','1000','500','333','300','100','45','15']
            for ii in range(len(Mcmds)):
                Mcm = Mcmds[ii]
                Mcm_answ = Mcmds_answs[ii]
                if Mcm in line and not gotkey:
                    print 'Got keyword: ',Mcm
                    answer=[Mcm_answ]+deepcopy(brewer_something)
                    gotkey = True


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
        print 'No key found for line:', str(line.replace('\r','\\r').replace('\n','\\n').replace('\x00','null'))

    return gotkey, answer

line_counter=0

# Open serial connection with COM15
print 'Opening serial connection...'
sw = serial.Serial('COM15', baudrate=1200, timeout=1)
#this is for changing the end of line detection
sio = io.TextIOWrapper(io.BufferedRWPair(sw, sw))

time.sleep(1)
sw.flushInput()

b_initialized=False
n_counter=0 #This is only to answer only to the last carriage return,
# when some of them are received in the initial connection with the brewer
print 'Done. Monitoring serial...'
with sw:
    while True:
        try:
            line = sio.readline()

            if not line:
                #print 'Line received: None data'
                # HACK: Descartamos líneas vacías porque fromstring produce
                # resultados erróneos, ver
                # https://github.com/numpy/numpy/issues/1714
                continue
            else:
                line_counter = line_counter + 1
                print str(line_counter), ' Line received:', str(line.replace('\r','\\r').replace('\n','\\n'))

                gotkey, answer = check_line(line)

                if gotkey:
                    b_initialized = True
                    if not b_initialized:
                        #Ignore the first 4 carriage returns to have brewer initialized
                        if line == '\n':
                            n_counter=n_counter+1
                            if n_counter < 4:
                                print 'Ignoring the first \\n ('+str(n_counter)+'/3)'
                            if n_counter == 4 or n_counter==8:
                                print 'Brewer initializated'
                                b_initialized=True
                    if b_initialized:
                        print 'Writting to com port:', str(answer)
                        for a in answer:
                            if 'wait' in a:
                                time.sleep(float(a.split('wait')[1]))
                            elif 'flush' in a:
                                sio.flush()
                            else:
                                sio.write(unicode(a))
                            #time.sleep(0.01)

        except ValueError:
            warnings.warn("Line {} didn't parse, skipping".format(line))
        except KeyboardInterrupt:
            print("Exiting")
            break