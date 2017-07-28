class Element():

    """This file builds a class called Element. When functions from database.py 
    create an object of Element, they are automatically stored alongside the data
    that we use to build our POTCAR files. This is then fed to another function that
    concatenates all the potcar files stored here into the final potcar file used 
    by VASP"""

    
    name = ""
    potcar = ""
    potdir = ""

    def __init__(self, name):

        self.name = name
        self.potdir = "/fslhome/glh43/src/potpaw_PBE/" + name + "/POTCAR"
        

        with open(self.potdir, 'r') as f:
            self.potcar = f.read()

        return
