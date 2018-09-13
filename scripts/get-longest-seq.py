import sys
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description='Gets largest fasta sequence from EMBOSS getorf.')
parser.add_argument('sequences', type=str, help='fasta file from getorf')
args = parser.parse_args()

currentSeq = ''
seqDict = dict()

with open(args.sequences,'r') as seqs:
    for record in SeqIO.parse(seqs,'fasta'):
        id = record.id.split('_')[0]
        if id not in seqDict:
            # currentSeq = record
            seqDict[id] = dict()
            seqDict[id]['description'] = record.description
            seqDict[id]['seq'] = record.seq
        elif len(record.seq) > len(seqDict[id]['seq']):
            seqDict[id]['description'] = record.description
            seqDict[id]['seq'] = record.seq

for key in seqDict:
    print(''.join(['>',key,' ',seqDict[key]['description'],'\n',str(seqDict[key]['seq'])]))

        # print(record)
