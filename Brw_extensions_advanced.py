from pcbasic.basic import Session


class ExtendedSession(Session):
    def __init__(self):
        Session.__init__(self, stdio=True, extension=self)

    def getHF_session(self):
        hf = self.get_variable("HF%")
        return hf

    def setHF_session(self, value):
        self.set_variable("HF%", value)


def HFswitch():
    with ExtendedSession() as s:
        HF = s.getHF_session()
        if HF == 10:
            s.setHF_session(0)
        elif HF == 0:
            s.setHF_session(1)
    return ""