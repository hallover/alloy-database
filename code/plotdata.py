
from matplotlib import pyplot as plt
import numpy as np

base = 92
path = "/fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN/"

EATOM = []
PSCENC = []
TOTEN = []
TEWEN = []
EBANDS = []
SIGMA0 = []
nENTRO = []
CPUTIME = []
IRRKPTS = []


with open(path + "EBANDS.txt", "r") as f:
    for line in f.readlines():
        EBANDS.append(float(line))

with open(path + "energySigma0.txt", "r") as f:
    for line in f.readlines():
        SIGMA0.append(float(line))

with open(path + "PSCENC.txt", "r") as f:
    for line in f.readlines():
        PSCENC.append(float(line))

with open(path + "TEWEN.txt", "r") as f:
    for line in f.readlines():
        TEWEN.append(float(line))

with open(path + "TOTEN.txt", "r") as f:
    for line in f.readlines():
        TOTEN.append(float(line))
errorTOTEN = []
for i in TOTEN:
    errorTOTEN.append(abs(i-TOTEN[base]))

        
with open(path + "EATOM.txt", "r") as f:
    for line in f.readlines():
        EATOM.append(float(line))

with open(path + "noEntropy.txt", "r") as f:
    for line in f.readlines():
        nENTRO.append(float(line))

with open(path + "cputime.txt", "r") as f:
    for line in f.readlines():
        CPUTIME.append(float(line))

with open(path + "irrkpts.txt", "r") as f:
    for line in f.readlines():
        IRRKPTS.append(float(line))

"""Now we're going to plot the data"""
base = 92 #line number 93 is the 43x43x43 kpt grid

#print(TOTEN[base])


print(errorTOTEN)

plt.scatter(IRRKPTS, errorTOTEN)
#plt.loglog()
plt.xlabel("# of Irreducible Kpoints")
plt.ylabel("Error")
plt.title("nKpoints vs error")
plt.savefig('graph1.pdf', bbox_inches='tight')


plt.scatter(IRRKPTS, CPUTIME)
plt.xlabel("Irreducible Kpoints")
plt.ylabel("Time")
plt.savefig('graph2.pdf', bbox_inches='tight')

#plt.scatter(
