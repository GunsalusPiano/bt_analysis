#!/bin/sh
#PBS -v PATH
#$ -v PATH


para=$1
cd /home/jovyan/data/crickmore/cry
./all-cry-aa.fasta.60-bl.pl 0 $para &
wait

