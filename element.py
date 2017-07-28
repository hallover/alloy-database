class Element():
    
    name = ""
    potcar = ""
    potdir = ""

    def __init__(self, name):

        self.name = name
        self.potdir = "/fslhome/glh43/src/potpaw_PBE/" + name + "/POTCAR"
        

        with open(self.potdir, 'r') as f:
            self.potcar = f.read()

        return
