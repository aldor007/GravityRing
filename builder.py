class SolarSystemBuilder(object):
    def __init__(self):
        self.system = None
    def addElement(self, obj):
        raise NotImplemented("Virtual metod")
    def constuct(self):
        raise NotImplemented("Virtual method")
    def getSystem(self):
        if self.system is None:
            self.constuct()
        return self.system


class ConfBuilder(SolarSystem):

    def __init__(self, filename):
        super(ConfBuilder, self).__init__()
        self.filename = filename

    def addElement(self, obj):
        self.system.append(obj)
    def constuct(self):
        

