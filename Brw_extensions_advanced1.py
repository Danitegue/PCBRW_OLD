from pcbasic.basic import Session


class ExtendedSession(Session):
    def __init__(self):
        Session.__init__(self, stdio=True, extension=self)

    def getHF_session(self):
        hf = self.get_variable("HF%")
        return hf


def HFswitch():
    with ExtendedSession() as s:
        HF = s.getHF_session()
        if HF == 1:
            HF=0
        elif HF == 0:
            HF=1
    return HF