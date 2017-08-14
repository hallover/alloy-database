#!/bin/bash

#awk '/free energy/ {e = $5}; END {print e}' OUTCAR >> temp.txt

#for directory in /fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN/10frzkpts/*/OUTCAR; do
 #   awk '/free energy/ {e = $5}; END {print e}' OUTCAR >> /fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN/10frzkpts/temp.txt
#done

cd /fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN/
find . -name OUTCAR -exec awk '/free energy/ {energy = $5}; END {print FILENAME " " energy}'{}\;

#for directory in ls -d /fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN/
#do

find . -name OUTCAR -exec awk '/free energy/ {energy = $5}; END {print FILENAME " " energy}' {} \; >> fenergy.txt

find . -name OUTCAR -exec awk '/free energy/ {energy = $5}; END {print FILENAME " " energy}' {} \; >> 
