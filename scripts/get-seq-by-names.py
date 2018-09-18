import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description='Gets sequences by name(s).')
parser.add_argument('-s','--sequences', type=str, help='fasta file', required=True)
parser.add_argument('-n','--names', type=str, nargs='+', help='fasta file', required=True)
args = parser.parse_args()

# print(args.names)
seqs = list()
with open(args.sequences, 'r') as f:
    for record in SeqIO.parse(f, 'fasta'):
        if record.id in args.names:
            seqs.append(record)
            # SeqIO.write(record,'out.fasta','fasta')

SeqIO.write(seqs,'out.fasta','fasta')
