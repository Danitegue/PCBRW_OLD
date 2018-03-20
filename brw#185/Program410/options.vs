55555 ' set to 0/1
4 AUTOHG=1
55555 ' FW2: set HIFW2 to 0/1/-1 for going to LOWER/OSCILATE/HIGHER neutral density when testing intensity
55555 ' FW2 for HG: set HGFW2 to 0 if want to have FW2 at 0 all the time or set it to 1 to set FW2 during HG same as SL
5 HIFW2=0:  HGFW2 = 1
55555 ' LATTN! variable sets the lower limit for count rate at 1 cycle that is acceptable before switching to higher FW2 position. STANDARD is 80000 
55555 ' UATTN! variable sets the upper limit for count rate at 1 cycle that is acceptable before switching to lower  FW2 position. STANDARD is 25000
55555 REM unrem the second assignment to go to standard attenuation decisions
6 LATTN!=35000!: UATTN! = 125000!: LATTN!=25000!: UATTN! = 80000!
7 REFLAG% = 0: NEED.HG = 0: NEED.FR = 0: HP.NOTDONE=1: RELH=-99: ATP=-99: RH=-99: AH=-99: EXT=-99: BC%=7: BC0%=7: CUB.U=1
55555 REM
55555 REM OPT.LOWDS: if 1 then DS will be skipped if less than 500 counts measured in 1 cycle at ND = 0; 
8 OPT.LOWDS = 1 
