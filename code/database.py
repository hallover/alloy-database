import os
from os.path import isfile, join
import zipfile as Z

"""We're going to use this script a lot. What I've been doing for 
developmental purposes is running python from the terminal, 
importing this module, and running the functions individually.

ex. -bash-4.1$ python
         >>> import database as d
         >>> d.getFILES()
         >>> d.buildDIRS()
         ... 
     you get the picture.

I'm going to include notes all throughout the code to help you 
to understand what's going on, because I wrote this code specifically
for my filesystem and never expected it to be seen by other people.
That's why its a convoluted mess.

Here's some definitions for you

VASP - Density Functional Theory package
  Input files:
    INCAR  = Specifies how we are going to do each process.
    POSCAR = Describes the location and species of each atom
        in the cell.
    POTCAR = Supplies Vasp with the pseudopotential for each atom,
        which must be in the same order as the listed elements of the POSCAR. 
        However, that is only necessary if we are trying to learn about a metal,
        which is not what we're doing. We're looking for patterns, so it's non-vital.
    KPOINTS = Tells vasp how dense of a grid we will be using and supplies
        the lattice vectors and universal scaling constant.
  Output files:
    OUTCAR = This is the main file we are looking at. Contains the calculated 
       energy levels for each run.
    IBZKPT = Gives us the number and location of each irreducible k-point






"""

zipfiles = []
pscrList = []                                                                                     
kptList = []
ptcrSpecList = []    
name = []
pscrList = []

inputzips = []

zippath = "/fslhome/holiver2/work/vasp/alloydatabase/alloyzips/"
newpath = "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"
finishedpath = "/fslhome/holiver2/work/vasp/alloydatabase/finished/"


def buildDIRS():
    """Once we have the zip files all in the /alloyzips folder, 
    we are going to run this function. It builds the directory tree and
    creates all of the input files for VASP.
    

    """


#    zippath = "/fslhome/holiver2/work/vasp/alloydatabase/alloyzips/"
#    newpath = "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"

    
    """Set up directory loop"""
    dirs = [d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d))]
    index = 0


#    print(inputzips)
    #print(len(pscrList))
    for metal in sorted(dirs):
        path = newpath + metal
        print(path)
#        print(pscrList[index])
        for n in range(4,45,3):
            lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"
            if not os.path.exists(lvl2path):
                os.makedirs(lvl2path)
            else:
                break 

            for k in range(n,44,3):
                lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"
                if not os.path.exists(lvl3path):
                    os.makedirs(lvl3path)

                """Here we're going to make each of the input files by calling 
                the functions declared later in this package"""

                getPOTCAR(lvl3path, index)

                with open(lvl3path + "/POSCAR" , "w") as f:
                    f.write(inputzips[index][1])

                #with open(lvl3path + "/preINCAR", "w") as f:
                 #   f.write(incrList[index])
                
                if k == n:
                    first = True
                else:
                    first = False

                makeINCAR(lvl3path, first, index)
                makeKPOINTS(lvl3path, k)
                makeSlurm(lvl3path, n, k, metal)
     #   print(index)
        #print(incrList[index])
        index += 1
    return


def getFILES():
#    zippath = "/fslhome/holiver2/work/vasp/alloydatabase/alloyzips/"
#    newpath = "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"
    zipnames = [f for f in os.listdir(zippath) if isfile(join(zippath,f))]
    
    global ptcrSpecList
    global inputzips
    name = []
    
    for nfile in range(0,len(zipnames)):
        zipfiles.append(Z.ZipFile(zippath + zipnames[nfile]))
        inside = Z.ZipFile.namelist(zipfiles[nfile])
        
        pscrList.append(Z.ZipFile.read(zipfiles[nfile],inside[0]))
        kptList.append(inside[1])
        incrList.append(Z.ZipFile.read(zipfiles[nfile],inside[2]))
#        print(incrList[nfile])

        spec = Z.ZipFile.read(zipfiles[nfile],inside[3])
        ptcrSpecList.append(spec.split()) # removed sorted()
        name.append("".join(ptcrSpecList[nfile]))


    inputzips = sorted(zip(name,pscrList,kptList,incrList,ptcrSpecList))
#    print(inputzips)

#    for i in inputzips:
        #print(i)
#        print("\n")
        
    for nfile in range(0,len(inputzips)):
        #print(ptcrSpecList[nfile])
        #print(incrList[nfile])
        #dirpath = newpath + str(nfile).zfill(2) + "-" + name[nfile]

        #print(inputzips[nfile][0])
        dirpath = newpath + name[nfile]
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    return

def getPOTCAR(path, index):

    #print(ptcrSpecList)
    from element import Element
    potpath = path + "/POTCAR"
#    print(index)
 #   print(inputzips[index][4])
    formula = inputzips[index][4] #chooses the potcarspec list from the sorted directory 'inputzips'
    
    
    elements = []
    
    for chem in formula:
        elements.append(Element(chem))

    with open(potpath, 'w') as f:
        for e in elements:
            f.write(e.potcar)


    return
def makeKPOINTS(path, kpts):
    kptpath = path + "/KPOINTS"
    kpts = str(kpts) + " "
    zeros = str(0) + " " + str(0) + " " + str(0)

    with open(kptpath, "w") as f:
        f.write("KPOINTS FILES\n")
        f.write("0\n")
        f.write("Monkhorst-Pack\n")
        kptstr = kpts + kpts + kpts
        f.write(kptstr + "\n")
        f.write(zeros)
    return


def makeINCAR(path, first, index):
    incarpath = path + "/INCAR"

    with open(incarpath, "w") as f:
        incarstr = inputzips[index][3]
        
        incarstr = incarstr.replace("NELM = 100","NELM = 50")
        incarstr = incarstr.replace("NSW = 99", "NSW = 1")
        incarstr = incarstr.replace("ISIF = 3", "ISIF = 0")
        



        if first == True:
            f.write(incarstr.replace("ICHARG = 1","ICHARG = 0"))
            
            
        else:
            f.write(incarstr.replace("ICHARG = 1", "ICHARG = 11"))

        
            
        """
    This is the custom INCAR I made. It doesn't work very well.
        f.write("ISTART = 0 \n")
        f.write("ISMEAR = -1\n")
        f.write("SIGMA = .2\n")
        
        
        if first == True:
            f.write("ICHARG = 0\n")                                                   
        else:
            f.write("ICHARG = 11\n")
        f.write("ENCUT = 500\n")
        
        f.write("ALGO = NORMAL \n")
        f.write("IBRION = 2\n")
        f.write("PREC = H\n")
        f.write("NELMIN = 4\n")


        f.write("NSW = 1\n")
        #f.write("EDIFF = .0001\n")
        #f.write("EDIFFG = 0.001\n")
        f.write("POTIM = 1.0\n")
        f.write("ISIF = 4\n")
    """
    """        f.write("ALGO = Fast\n")
        f.write("EDIFF = 0.00025\n")
        f.write("ENCUT = 520\n")
        f.write("IBRION = 2\n")
        if first == True:
            f.write("ICHARG = 1\n")
        else:
            f.write("ICHARG = 11\n")
        f.write("ISIF = 3")"""


    return


def makeSlurm(path, frz, kpts, name):
    with open(path + "/RUN.sh", "w") as f:
        f.write("#!/bin/bash\n")
        
        """Better approximations for walltime and memory usage
        n < 10 ... 0:15:00, 1000M
        n < 20 ... 0:30:00, 2000M
        n < 30 ... 1:00:00, 3000M
        n > 30 ... 2:00:00, 6000M
        
        4*(NGXF/2+1)*NGYF*NGZF*16
        NKDIM*NBANDS*NRPLWV*16
        """
        if kpts == 4:
            f.write("#SBATCH --time=00:30:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=1000M   # memory per CPU core\n")
        elif kpts == 7:
            f.write("#SBATCH --time=01:00:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=2000M   # memory per CPU core\n")       
        elif kpts == 10 or kpts == 13:
            f.write("#SBATCH --time=02:00:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=4000M   # memory per CPU core\n") 
        elif kpts == 16 or kpts == 19:
            f.write("#SBATCH --time=03:00:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=8000M   # memory per CPU core\n")    
        elif kpts == 22 or kpts == 25:
            f.write("#SBATCH --time=04:00:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=8000M # memory per CPU core\n")
        elif kpts == 28 or kpts == 31:
            f.write("#SBATCH --time=06:00:00   # walltime\n")                        
            f.write("#SBATCH --mem-per-cpu=15000M   # memory per CPU core\n")
        elif kpts == 34 or kpts == 37:
            f.write("#SBATCH --time=08:00:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=30000M   # memory per CPU core\n") 
        elif kpts == 40 or kpts == 43:
            f.write("#SBATCH --time=12:00:00 # walltime\n")
            f.write("#SBATCH --mem-per-cpu=60000M # memory per CPU core\n")

            

        
        f.write("#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)\n")
        f.write("#SBATCH --nodes=1   # number of nodes\n")
        
        f.write("#SBATCH -J " + name[0] +"-"+ str(frz).zfill(2) +"-"+ str(kpts).zfill(2) +" #job name\n")
        f.write("#SBATCH --mail-user=haydenoliver@physics.byu.edu #email\n")
        f.write("#SBATCH --mail-type=FAIL\n")
        #f.write("#SBATCH --gid=glh43physicsnodes\n")
        
        f.write("# Compatibility variables for PBS. Delete if not needed.\n\n")
        f.write("export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`\n")
        f.write("export PBS_JOBID=$SLURM_JOB_ID\n")
        f.write("export PBS_O_WORKDIR=\"$SLURM_SUBMIT_DIR\"\n")
        f.write("export PBS_QUEUE=batch\n")

        f.write("# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.\n")
        f.write("export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE\n")

        f.write("#LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE\n")
        f.write("cd " + path + "; vasp5.x")





def runFirstBatch():
#    zippath = "/fslhome/holiver2/work/vasp/alloydatabase/alloyzips/"
#    newpath = "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"
    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath,d))])
    index = 0
    for metal in range(len(dirs)):   
        path = newpath + dirs[metal]
        print(dirs[metal])


        userinput = input("y (1) or n (0): ")
        if userinput == 1:
            for n in range(4,45,3):
                lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"
                for k in range(n,44,3):
                    lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"    
                    if k == n:
                        
                        os.system("cd " + lvl3path + "; sbatch RUN.sh")
        else:
            keepgoing = 1
        
            


def cpCHGCAR():
#    newpath= "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"

    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath,d))])

    for metal in range(len(dirs)):
        path = newpath + dirs[metal]
        print(path)

        userinput = input("y (1) or n (0): ")
        if userinput == 1:
        
            for n in range(4,45,3):
                lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"
                print(n)
                os.system("for d in " + lvl2path + "/*/; do cp " +lvl2path + "/" + str(n).zfill(2) + "kpts/CHGCAR \"$d\"; done")

                #for k in range(n,44,3):
                 #   lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"
                
            
        else:
            zzz = 1
                

def readOUTCAR():
#    newpath = "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"
    
    for metal in sorted(dirs):
        path = newpath + metal
        print(path)

        for n in range(4,45,3):
            n = 1
                    
def editSlurm():
#    zippath = "/fslhome/holiver2/work/vasp/alloydatabase/alloyzips/"
#    newpath = "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"


    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d))])


    for metal in range(len(dirs)):                                                      
        path = newpath + dirs[metal]
        print(path)

        userinput = input("y (1) or n (0): ")
        if userinput == 1:
            
            for n in range(4,45,3):
                lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"
                for k in range(n,44,3):
                    lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"

                    makeSlurm(lvl3path, n, k, dirs[metal])                                     
        else:
            zzz = 1        
                                                                          
    return


def gatherData():

    """This function is still in development, hence the very specific and non-dynamic instructions.
Once it is finished, we will have the ability to read the data from all the vasp runs"""

    
#    newpath = "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"
    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d))])

    freeEnergy = []
    eNoEntropy = []
    atomicEnergy = []
    ewaldEnergy = []
    energySigma0 = []
    totalCPUtime = []
    for metal in range(len(dirs)):
        #path = newpath + dirs[metal]
        path = "/fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN"
        print(dirs[metal])
        userinput = input("1 = yes, 0 = no")
        if userinput == 1:
            for n in range(4,45,3):
                lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"
                
                for k in range(n,44,3):
                    lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"
                    #lvl3path = path
                    
                    outcarpath = lvl3path + "/OUTCAR"
                    ibzkptpath = lvl3path + "/IBZKPT"

                    mylines = ""
                    with open(outcarpath, 'r') as f:
                        mylines = f.readlines()
                    mylines.reverse()
                    #print(k)
                    for line in mylines:
                    #print(line)
                        if "free energy    TOTEN" in line:
                        
                            freeEnergy.append(line)
                        if "energy without entropy " in line:
                            eNoEntropy.append(line)
                        if "atomic energy " in line:
                            atomicEnergy.append(line)
                        if "Ewald energy " in line:
                            ewaldEnergy.append(line)
                        if "Total CPU time used " in line:
                            totalCPUtime.append(line)
                        

                resultspath = "/fslhome/holiver2/work/vasp/alloydatabase/finished/" + dirs[metal] + "RESULTS.txt"
                
            splitFreeEnergy = []



            with open(resultspath, "w") as f:
                for i in freeEnergy:
                    f.write(i)
                    f.write(", ")
            
        
            for i in freeEnergy:
                splitFreeEnergy.append(i.split())
            #print(splitFreeEnergy[::5])
            for i in splitFreeEnergy:
                print(i[4])
    
    return


def runSecondBatch():
#    newpath = "/fslhome/holiver2/work/vasp/alloydatabase/metalsdir/"
    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d))])

    for metal in range(len(dirs)):
        path = newpath + dirs[metal]

        print(dirs[metal])
        userinput = input("yes (1), no (0): ")

        if userinput == 1:
            for n in range(4,45,3):
                print(str(n) + " frozen kpoints")
                
                lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"
                for k in range(n,44,3):
                    
                    lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"    
                    """
                    outcarpath = lvl3path + "/OUTCAR"

                    if os.path.exists(outcarpath):
                    
                        with open(outcarpath, "r") as f:
                            for line in f:
                                redo = False
                                if "General timing and accounting informations" in line:
                                   # os.system("cd " + lvl3path + "; sbatch RUN.sh")
                                    redo = False
                                    break
                                else:
                                    redo = True

                                if redo == True:
                                    os.system("cd " + lvl3path + "; sbatch RUN.sh")
                    """                                    
                    if n != k:
                        os.system("cd " + lvl3path + "; sbatch RUN.sh")         
        else:
            zzz = 1        
    return

def copyData():
    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath,d))])

    for metal in range(len(dirs)):
        

        path = newpath + dirs[metal] + "/"

        print(dirs[metal])
        userinput = input("yes - 1: no - 0")
    
        if userinput == 1:
            os.system("rsync -r " + path + " " + finishedpath + dirs[metal])

        else:
            zzz = 1
