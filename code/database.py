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


import os
import zipfile as Z
from os.path import isfile, join
from getpass import getuser
from matplotlib import pyplot as plt





zipfiles = []
pscrList = []
incrList = []     
kptList = []
ptcrSpecList = []    
name = []
pscrList = []

inputzips = []


netID = getuser()


zippath = "/fslhome/" + netID + "/vasp/alloydatabase/alloyzips/"
newpath = "/fslhome/" + netID + "/vasp/alloydatabase/metalsdir/"
finishedpath = "/fslhome/" + netID + "/vasp/alloydatabase/finished/"
databasepath = "/fslhome/" + netID + "/vasp/database/code/"

def buildDIRS():
    #Once we have the zip files all in the /alloyzips folder, we are going to run this function.
    #It builds the directory tree and creates all of the input files for VASP.
    
    #Set up directory loop
    dirs = [d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d))]
    index = 0

    for metal in sorted(dirs):
        path = newpath + metal
        print(path)

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

                #Here we're going to make each of the input files by calling 
                #the functions declared later in this package

                getPOTCAR(lvl3path, index)

                with open(lvl3path + "/POSCAR" , "w") as f:
                    f.write(inputzips[index][1])

                
                if k == n:
                    first = True
                else:
                    first = False

                makeINCAR(lvl3path, first, index)
                makeKPOINTS(lvl3path, k)
                makeSlurm(lvl3path, n, k, metal)

        index += 1
    return


def getFILES():

    zipnames = [f for f in os.listdir(zippath) if isfile(join(zippath,f))]
    
#    global ptcrSpecList
    global inputzips
    name = []
    
    for nfile in range(0,len(zipnames)):
        zipfiles.append(Z.ZipFile(zippath + zipnames[nfile]))
        inside = Z.ZipFile.namelist(zipfiles[nfile])
        
        pscrList.append(Z.ZipFile.read(zipfiles[nfile],inside[0]))
        kptList.append(inside[1])
        incrList.append(Z.ZipFile.read(zipfiles[nfile],inside[2]))

        spec = Z.ZipFile.read(zipfiles[nfile],inside[3])
        ptcrSpecList.append(spec.split()) # removed sorted()
        name.append("".join(ptcrSpecList[nfile]))


    inputzips = sorted(zip(name,pscrList,kptList,incrList,ptcrSpecList))
        
    for nfile in range(0,len(inputzips)):

        dirpath = newpath + name[nfile]
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    with open(databasepath + "namelist.txt", "w") as f:
        for entry in sorted(name):
            f.write(entry)
            f.write("\n")
            
    return

def getPOTCAR(path, index):


    from element import Element
    potpath = path + "/POTCAR"

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

#    with open(incarpath, "w") as f:
#        incarstr = inputzips[index][3]
        
#        incarstr = incarstr.replace("NELM = 100","NELM = 50")
#        incarstr = incarstr.replace("NSW = 99", "NSW = 1")
#        incarstr = incarstr.replace("ISIF = 3", "ISIF = 0")
#        incarstr = incarstr.replace("ISPIN = 2", "ISPIN = 1")

#        f.write("NBANDS = 100\n")
#        f.write("LMAXMIX = 4\n")
    with open(incarpath, "w") as f:
        f.write("IBRION = 2\n")
        f.write("ISIF = 5\n")
        f.write("ISMEAR = -1\n")
        f.write("SIGMA = .001\n")
        f.write("NSW = 100\n")
        f.write("POTIM = 0.5\n")
        f.write("ENCUT = 400\n")
        f.write("PREC = Accurate\n")
        f.write("NBANDS = 100\n")
        f.write("EDIFF = .00000001\n")
        f.write("LMAXMIX = 2\n")


        if first == True:
            #f.write(incarstr.replace("ICHARG = 1","ICHARG = 0"))
            f.write("ICHARG = 1\n")
            
        else:
            #f.write(incarstr.replace("ICHARG = 1", "ICHARG = 11"))
            f.write("ICHARG = 11\n")

    return


def makeSlurm(path, frz, kpts, name):
    with open(path + "/RUN.sh", "w") as f:
        f.write("#!/bin/bash\n")

        f.write("#SBATCH --partition=physics \n")
        
        if kpts == 4:
            f.write("#SBATCH --time=00:10:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=1000M   # memory per CPU core\n")
        elif kpts == 7:
            f.write("#SBATCH --time=00:20:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=2000M   # memory per CPU core\n")       
        elif kpts == 10 or kpts == 13:
            f.write("#SBATCH --time=00:40:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=4000M   # memory per CPU core\n") 
        elif kpts == 16 or kpts == 19:
            f.write("#SBATCH --time=01:30:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=6000M   # memory per CPU core\n")    
        elif kpts == 22 or kpts == 25:
            f.write("#SBATCH --time=02:20:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=9000M # memory per CPU core\n")
        elif kpts == 28 or kpts == 31:
            f.write("#SBATCH --time=03:30:00   # walltime\n")                        
            f.write("#SBATCH --mem-per-cpu=10000M   # memory per CPU core\n")
        elif kpts == 34 or kpts == 37:
            f.write("#SBATCH --time=04:30:00   # walltime\n")
            f.write("#SBATCH --mem-per-cpu=12000M   # memory per CPU core\n") 
        elif kpts == 40 or kpts == 43:
            f.write("#SBATCH --time=5:30:00 # walltime\n")
            f.write("#SBATCH --mem-per-cpu=18000M # memory per CPU core\n")

            

        
        f.write("#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)\n")
        f.write("#SBATCH --nodes=1   # number of nodes\n")
        
        f.write("#SBATCH -J " + name +"-"+ str(frz).zfill(2) +"-"+ str(kpts).zfill(2) +" #job name\n")
        f.write("#SBATCH --mail-user=haydenoliver@physics.byu.edu #email\n")
        f.write("#SBATCH --mail-type=FAIL\n")

        
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

    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath,d))])
    
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
                        redoJob = True
                        if os.path.isfile(lvl3path + "/OUTCAR"):
                            with open(lvl3path + "/OUTCAR", "r") as f:
                                for line in f.readlines():
                                    if "General timing and accounting informations" in line:
                                        redoJob = False
                                        print(n,k,"Complete")
                                        os.system("for d in " + lvl2path + "/*/; do cp " + lvl2path + "/" + str(n).zfill(2) + "kpts/CHGCAR \"$d\"; done")                      
                        if redoJob == True:
                            os.system("cd " + lvl3path + "; sbatch RUN.sh")


def cpCHGCAR():


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



def editSlurm():

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
                                                                          
    return

def editIncar():
    getFILES()
    dirs = sorted ([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d))])

    for metal in range(len(dirs)):
        path = newpath + dirs[metal]
        print(path)

        userinput = input("y (1) ur n (0): ")
        if userinput == 1:
            for n in range(4,45,3):
                lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"
                for k in range(n,44,3):
                    lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"

                    if k == n:
                        first = True
                    else:
                        first = False

                    makeINCAR(lvl3path,first,metal)


def gatherData():
    
    newpath = "/fslhome/" + netID + "/vasp/alloydatabase/metalsdir/"
    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d))])

    for metal in range(len(dirs)):
        name = dirs[metal]
        
        freeEnergy = []
        eNoEntropy = []
        atomicEnergy = []
        ewaldEnergy = []
        energySigma0 = []
        irrkpts = []
        totalCPUtime = []
        setloc = []
        alphaz = []
        eigenvalues = []
        
        #path = "/fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN"
        path = newpath + dirs[metal]
        print(dirs[metal])
        userinput = input("1 = yes, 0 = no")
        if userinput == 1:
            for n in range(4,45,3):
                lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"
                
                for k in range(n,44,3):
                    lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"
        
                    
                    outcarpath = lvl3path + "/OUTCAR"
                    #ibzkptpath = lvl3path + "/IBZKPT"
              #      if not os.path.isdir(outcarpath):
              #          print("nope")
              #          break
                    mylines = ""
                    with open(outcarpath, 'r') as f:
                        mylines = f.readlines()
#                    mylines.reverse()
        
                    for line in mylines:
        
                        if "free energy    TOTEN" in line:
                            freeEnergy1 = line
                         
                        if "energy without entropy " in line:
                            eNoEntropy1 = line
                            
                        if "atomic energy  EATOM  =" in line:
                            atomicEnergy1 = line
                            
                        if "Ewald energy   TEWEN  =" in line:
                            ewaldEnergy1 = line
                            
                        if "Total CPU time used " in line:
                            totalCPUtime1 = line
                            
                        if "irreducible k-points:" in line:
                            irrkpts1 = line
                            
                        if "eigenvalues    EBANDS =" in line:
                            eigenvalues1 = line
                            
                        if "alpha Z        PSCENC" in line:
                            alphaz1 = line
                            
                        if "energy without entropy =" in line:
                            energySigma01 = line
                            
                    #Alldatazip order = kptorder,cputime,irrkpts,freeEnergy,ewaldEnergy,alphaZ,energySigma0,energyNoEntropy,eigenvalues

                    #print("TEST ")
                    freeEnergy.append(float(freeEnergy1.split()[4]))
                    eNoEntropy.append(float(eNoEntropy1.split()[4]))
                    atomicEnergy.append(float(atomicEnergy1.split()[4]))
                    ewaldEnergy.append(float(ewaldEnergy1.split()[4]))
                    totalCPUtime.append(float(totalCPUtime1.split()[5]))
                    irrkpts.append(int(irrkpts1.split()[1]))
                    setloc.append([n,k])
                    energySigma0.append(float(energySigma01.split()[7]))
                    alphaz.append(float(alphaz1.split()[4]))
                    eigenvalues.append(float(eigenvalues1.split()[3]))
            
            alldatazip = zip(setloc,totalCPUtime,irrkpts,freeEnergy,ewaldEnergy,alphaz,energySigma0,eNoEntropy,eigenvalues)
            print(len(alldatazip))

            #for i in alldatazip:
            #    print(i)
            #with open("1~/vasp/database/energy.txt","w") as f:
            #    f.write(freeEnergy)
            plotdata(alldatazip, path, name)
            del alldatazip[:]
            #for i in alldatazip:
        
    return

def plotdata(alldatazip, path, name):
    error_alldata = []
    for i in range(0,len(alldatazip)-1):
        A = []
        A.append(alldatazip[i][0])
             
        for j in range(1,len(alldatazip[-1])):
            a = abs(alldatazip[-1][j] - alldatazip[i][j])
            A.append(a)
        A[2] = alldatazip[i][2]
        error_alldata.append(A)

#    print(error_alldata)
   # for i in error_alldata:    
    #    print(i)

    for i in range(0,10):
        print(error_alldata[i])
    
    kpts = 4
    eTOTEN = []
    eTEWEN = []
    ePSCENC = []
    eSIGMA0 = []
    e_nENTRO = []
    eEBANDS = []
    ikpts = []   

    #Alldatazip order = kptorder,cputime,irrkpts,freeEnergy,tewen,pscenc,sigma0,nentro,ebands
    
    for h in range(0,14):
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        irrk = []
            
        #KPTORDER,CPUTIME,IRRKPTS,TOTEN,TEWEN,PSCENC,SIGMA0,nENTRO,EBANDS
        
        for i in range(len(error_alldata)):
            if error_alldata[i][0][0] == kpts:
                
                a.append(error_alldata[i][3])
                b.append(error_alldata[i][4])
                c.append(error_alldata[i][5])
                d.append(error_alldata[i][6])
                e.append(error_alldata[i][7])
                f.append(error_alldata[i][8])
                irrk.append(error_alldata[i][2])

        
            kpts = 3 * h + 4

            
        eTOTEN.append(a)
        eTEWEN.append(b)
        ePSCENC.append(c)
        eSIGMA0.append(d)
        e_nENTRO.append(e)
        eEBANDS.append(f)
        ikpts.append(irrk)


    #print(eTOTEN)
    del eTOTEN[0]
    del ikpts[0]
    del eSIGMA0[0]
    del e_nENTRO[0]
    del eEBANDS[0]
    del ePSCENC[0]
    del eTEWEN[0]

    #print(ikpts)     

    #errorset = [eTOTEN,eTEWEN,ePSCENC,eSIGMA0,e_nENTRO,eEBANDS]

    #print(ikpts)

    graphpath = "/fslhome/" + netID + "/vasp/database/code/graphs/"


    
    for i in range(len(ikpts)):
        plt.plot(ikpts[i],eTOTEN[i])
    plt.xlabel("Irreducible k-points")
    plt.ylabel("Error")
    plt.title(name + " TOTEN")
 #   plt.loglog()
    plt.savefig(graphpath + name + "_eTOTEN.pdf")
    plt.close()
    
    """for i in range(len(ikpts)):
        print(eTEWEN[i])
        plt.plot(ikpts[i], eTEWEN[i])
    plt.loglog()
    plt.xlabel("Irreducible k-points")
    plt.ylabel("Error")
    plt.title(name + " TEWEN")
    plt.savefig(graphpath + name + '_eTEWEN.pdf')
    plt.close()
    """
    for i in range(len(ikpts)):
        plt.plot(ikpts[i], eEBANDS[i])
#    plt.loglog()
    plt.xlabel("Irreducible k-points")
    plt.ylabel("Error")
    plt.title(name + " EBANDS")
    plt.savefig(graphpath + name + '_eEBANDS.pdf')
    plt.close()
    
    for i in range(len(ikpts)):
        plt.plot(ikpts[i], eSIGMA0[i])
#    plt.loglog()
    plt.xlabel("Irreducible k-points")
    plt.ylabel("Error")
    plt.title(name + " SIGMA -> 0")
    plt.savefig(graphpath + name + '_eSIGMA.pdf')
    plt.close()

    """for i in range(len(ikpts)):
        plt.plot(ikpts[i], ePSCENC[i])
    plt.loglog()
    plt.xlabel("Irreducible k-points")
    plt.ylabel("Error")
    plt.title(name + " PSCENC")
    plt.savefig(graphpath + name + '_ePSCENC')
    plt.close()"""
    
    for i in range(len(ikpts)):
        plt.plot(ikpts[i], e_nENTRO[i])
#    plt.loglog()
    plt.xlabel("Irreducible k-points")
    plt.ylabel("Error")
    plt.title(name + " No Entropy")
    plt.savefig(graphpath + name + '_e_nENTRO.pdf')
    plt.close()
    return


def runSecondBatch():

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

                    #if os.path.isfile(lvl3path + "/CHGCAR"):
                    if n != k:
                        redoJob = True 
                        if os.path.isfile(lvl3path + "/OUTCAR"):
                            with open(lvl3path + "/OUTCAR", "r") as f:
                                
                                for line in f.readlines():
                                #If line is detected in OUTCAR, do not resubmit job
                                    
                                    if "General timing and accounting informations" in line:
                                        redoJob = False
                                        print("Complete")
                        
                        if not os.path.isfile(lvl3path + "/CHGCAR"):
                            print("Resubmit batch 1")
                            redoJob = False
                            
                        if redoJob == True:
                            os.system("cd " + lvl3path + "; sbatch RUN.sh")         
                    
    return

def copyData():
    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath,d))])

    for metal in range(len(dirs)):
        

        path = newpath + dirs[metal] + "/"

        print(dirs[metal])
        userinput = input("yes - 1: no - 0")
    
        if userinput == 1:
            os.system("rsync -r " + path + " " + finishedpath + dirs[metal])

