import logging

from pcbasic.basic import Session

class ExtendedSession(Session):
    def __init__(self):
        Session.__init__(self, stdio=True, extension=self)

    def getHF2(self):
        hf=self.get_variable("HF%")
        print "HF%=",str(hf)
        return hf

    def adda(self, x):
        print "adda", repr(x), repr(self.get_variable("a"))
        return x + self.get_variable("a")

def duplicate(n):
    try:
        return 2*int(n)
    except IndexError:
        return -1

def getHF():
    try:
        with ExtendedSession() as s:
            HF=s.getHF2()
        return HF
    except IndexError:
        return -1