#!/bin/bash
set -e

[[ -z $1 ]] && echo ARFCN? && exit 1

hppm=23
arfcn=$1
cfile=/root/capture/$arfcn.cfile

echo capturing ARFCN $arfcn for 70 seconds into $cfile

#HRF
grgsm_capture --arfcn=$arfcn --ppm="$hppm" --args=hackrf=0 --gain=32 --cfile=$cfile --rec-length=140

ls -lhF $cfile

