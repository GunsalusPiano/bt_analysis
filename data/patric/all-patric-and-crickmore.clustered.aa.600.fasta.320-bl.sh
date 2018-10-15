#!/bin/sh
#PBS -v PATH
#$ -v PATH


para=$1
cd /home/jovyan/data/patric
./all-patric-and-crickmore.clustered.aa.600.fasta.320-bl.pl 0 $para &
wait

