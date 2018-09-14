import argparse
import re

parser = argparse.ArgumentParser(description='Renames Crickmore sequences to have more informative names.')
parser.add_argument('-s','--sequences', type=str, help='fasta file containing crickmore database sequences')
parser.add_argument('-t','--table', type=str, help='TSV table containing the accession in the second column and the toxin name in the first')
args = parser.parse_args()

toxinDict = dict()
with open(args.table, 'r') as f:
    for line in f.readlines():
        l = line.rstrip().split('\t')
        toxinDict[l[1]] = l[0]

with open(args.sequences, 'r') as seqs:
    for record in SeqIO.parse(seqs, 'fasta'):
        id = re.sub('pir\|\|','',record.id.split('.')[0]).rstrip()
        print(''.join(['>',toxinDict[id],' ',record.description,'\n',str(record.seq)]))
