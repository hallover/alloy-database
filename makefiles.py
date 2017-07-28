
# coding: utf-8




import os
from os.path import isfile, join
import zipfile as Z

#POTCARSPEC = []

def makeDirs():
    metalspath = "/fslhome/holiver2/work/vasp/alloydatabase/alloyzips/"
    allfiles = [f for f in os.listdir(metalspath) if isfile(join(metalspath,f))]

    nfiles = len(allfiles)
    
        
   newpath = r'/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    zf = ['' for string in allfiles]
    potcarSpec = ['' for string in allfiles]



    """This will create the potcarSpec list"""
    for nfile in range(0,len(allfiles)):
            
        zf[nfile] = (Z.ZipFile(metalspath + allfiles[nfile], 'r'))
        inside = Z.ZipFile.namelist(zf[nfile])

        spec = Z.ZipFile.read(zf[nfile],inside[3])
        potcarSpec[nfile] = spec.split()
        potcarSpec = sorted(potcarSpec)
        

        
    name = []
    for z in range(0, len(potcarSpec)):
        potcarSpec[z] = sorted(potcarSpec[z])
        print(potcarSpec[z])
        
        name.append("".join(potcarSpec[z]))
        if not os.path.exists(newpath + name[z]):
            os.makedirs(newpath + name[z])
    global POTCARSPEC
    POTCARSPEC = potcarSpec
    
            
    """WORKING UP TO HERE"""
    
    """Here we're going to start building the file structure within the metals directories.
    It will consist of several nested loops to add the necessary POTCAR, INCAR, KPOINTS, and POSCAR 
    files, so that each """

        
    dirs = [d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d ))]
    print(dirs)


    index = 0
    for q in dirs:
        path = newpath + q 
        
        
        for n in range(4,45,2):
            lvl2path = path + "/" + str(n) + "frzkpts" 
            if not os.path.exists(lvl2path):
                os.makedirs(lvl2path)

            for k in range(n,44,2):
                lvl3path = lvl2path + "/" + str(k) + "kpts"
                if not os.path.exists(lvl3path):
                    os.makedirs(lvl3path)

                createPotcar(potcarSpec[index], lvl3path)

                if k == n:                                                                              
                    first = True                                                                        
                else:                                                                                   
                    first = False            
                
                createIncar(lvl3path, first)
                createPoscar(lvl3path)
                createKpoints(lvl3path, k)
                    
                
        index = index + 1
        

def createIncar(path, first):
    incarpath = path + "/INCAR"
    with open(incarpath ,"w") as f:
#             for i in range(10):
#                 f.write("This is line %d\r\n" %(i+1))
        f.write("ALGO = Fast \n")
        f.write("EDIFF = 0.0005\n")
        f.write("ENCUT = 520\n")
        f.write("IBRION = 2\n")
        
        if first == True:
            f.write("ICHARG = 0\n")
        else:
            f.write("ICHARG = 11\n")
        
        f.write("ISIF = 3\n")
        f.write("ISMEAR = -5\n")
        f.write("ISPIN = 2\n")
        f.write("LDAU = True\n")
        f.write("LDAUJ = 0 0 0\n")
        f.write("LDAUL = 2 2 0\n")
        f.write("LDAUPRINT = 1\n")
        f.write("LDAUTYPE = 2\n")
#             f.write("LDAUU = 3.32 6.2 0")
#             f.write("LMAXMIX = 4")
        f.write("LORBIT = 11\n")
        f.write("LREAL = .FALSE.\n")
        f.write("LWAVE = False\n")
#             f.write("MAGMOM = 12*5.0 24*0.6")
        f.write("NELM = 100\n")
        f.write("NSW = 0\n")
        f.write("PREC = Accurate\n")
        f.write("SIGMA = 0.05\n")
    
        return
    
    
def createPoscar(path):
    poscarpath = /fslhome/holiver2/work/vasp/alloydatabase/alloyzips/
    pscrfiles = [f for f in listdir(poscarpath) if isfile(join(poscarpath,f))]

    
    
    return


def createKpoints(path, kpts):
    kptpath = path + "/KPOINTS"
    kpts = str(kpts) + " "
    zeros = str(0) + " " + str(0) + " " + str(0)
    with open(kptpath,"w") as f:
        f.write("KPOINTS FILE\n")
        f.write("0\n")
        f.write("Monkhorst-Pack\n")
        kptstr = kpts + kpts + kpts
        f.write(kptstr)
        f.write("\n")
        f.write(zeros)
    return


def createPotcar(potcarname, path):
    elementlist = potcarname
    elements = []
    from element import Element
    """ 'Element' is a class, and we are going to create an object for each element in the alloy
and combine their respective POTCAR files to create the final POTCAR
Create objects for each element in elementlist from potcar.spec"""
    for i in elementlist:
        elements.append(Element(i))

    potpath = path + "/POTCAR"
    with open(potpath, 'w') as f:
        for e in elements:
            f.write(e.potcar)
    return
        
        
        

    
def createSlurm(self):
    
    a = 1
    return
