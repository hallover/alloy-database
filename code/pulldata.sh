#!/bin/bash

awk '/free energy/ {e = $5}; END {print e}' OUTCAR >> temp.txt

for directory in /fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN/10frzkpts/*/OUTCAR; do
    awk '/free energy/ {e = $5}; END {print e}' OUTCAR >> /fslhome/holiver2/work/vasp/alloydatabase/finished/0-CdCoN/10frzkpts/temp.txt
done
