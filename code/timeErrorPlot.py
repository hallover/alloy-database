import os as os
import zipfile as Z
from os.path import isfile, join
from getpass import getuser
from matplotlib import pyplot as plt

zipfiles = []
kptList = []
name = []

inputzips = []


netID = getuser()


zippath = "/fslhome/" + netID + "/vasp/alloydatabase/alloyzips/"
newpath = "/fslhome/" + netID + "/vasp/alloydatabase/metalsdir/"
finishedpath = "/fslhome/" + netID + "/vasp/alloydatabase/finished/"
databasepath = "/fslhome/" + netID + "/vasp/database/code/"


def plotData(freeEnergy, setloc, totalCPUtime, path, name):
    error_alldata = []
    for i in range(0, len(freeEnergy) - 1):
        A = []
        A.append(freeEnergy[i])
        

        for j in range(1, len(freeEnergy)):
            a = abs(freeEnergy[len(freeEnergy)-1] - freeEnergy[i])
            A.append(a)
        #A[2] = alldatazip[i][2]
        error_alldata.append(A)


    kpts = 4
    eTOTEN = []
    #ikpts = []

    for h in range(0, 14):
        a = []
        irrk = []

        for i in range(len(freeEnergy)):
            if setloc[i] == kpts:

                a.append(error_alldata[i])
               # irrk.append(error_alldata[i][2])


 #               print(error_alldata[i][0][0])


            kpts = 3 * h + 4
#        print(kpts)

           
        eTOTEN.append(a)
        #ikpts.append(irrk)
    
    del totalCPUtime[0]
    del eTOTEN[0]
    #del ikpts[0]
    print(totalCPUtime)
    print(eTOTEN)

    graphpath = "/fslhome/" + netID + "/vasp/database/code/graphs/"

#    print(eTOTEN)
   # print(totalCPUtime)

    for i in range(len(freeEnergy)):
  #      print(etoten[0][i])
   #     print(totalCPUtime[i])
        for j in range(len(freeEnergy[i]))
           plt.plot(eTOTEN[i][j], totalCPUtime[i])
    plt.loglog()
    plt.xlabel("Error")
    plt.ylabel("CPU Usage Time")
    plt.title(name + "Time-Error Efficiency")
    plt.savefig(graphpath + name + '_kpts.pdf')
    plt.close()

    return



def gatherData():
    newpath = "/fslhome/" + netID + "/vasp/alloydatabase/metalsdir/"
    dirs = sorted([d for d in os.listdir(newpath) if os.path.isdir(os.path.join(newpath, d))])

    for metal in range(len(dirs)):
        name = dirs[metal]

        freeEnergy = []
 #       irrkpts = []
        totalCPUtime = []
        setloc = []


        # path = "/fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN"
        path = newpath + dirs[metal]
        print(dirs[metal])
        userinput = input("1 = yes, 0 = no")
        if userinput == 1:
            for n in range(4, 45, 3):
                lvl2path = path + "/" + str(n).zfill(2) + "frzkpts"

                for k in range(n, 44, 3):
                    lvl3path = lvl2path + "/" + str(k).zfill(2) + "kpts"

                    outcarpath = lvl3path + "/OUTCAR"

                    with open(outcarpath, 'r') as f:
                        mylines = f.readlines()

                    for line in mylines:

                        if "free energy    TOTEN" in line:
                            freeEnergy1 = line

                        if "Total CPU time used " in line:
                            totalCPUtime1 = line

                        if "irreducible k-points:" in line:
                            irrkpts1 = line


                    freeEnergy.append(float(freeEnergy1.split()[4]))
                    totalCPUtime.append(float(totalCPUtime1.split()[5]))
                    setloc.append([n,k])
#                    irrkpts.append(int(irrkpts1.split()[1]))

  #              alldatazip = zip(setloc, totalCPUtime, irrkpts, freeEnergy)
                
#                print(setloc)
 #               print(totalCPUtime)
                plotData(freeEnergy, setloc, totalCPUtime, path, name)
 #               del alldatazip[:]
                print("happy Kennedy")
                     
    return
