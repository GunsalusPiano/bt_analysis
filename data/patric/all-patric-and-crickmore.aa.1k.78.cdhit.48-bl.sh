#!/bin/sh
#PBS -v PATH
#$ -v PATH


para=$1
cd /home/jovyan/data/patric
./all-patric-and-crickmore.aa.1k.78.cdhit.48-bl.pl 0 $para &
wait

