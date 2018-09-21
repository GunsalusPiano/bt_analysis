import sys
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description='Filters sequences by length.')
parser.add_argument('-s','--sequences', type=str, help='fasta file from getorf', required=True)
parser.add_argument('-l','--length', type=int, help='Minimum length cutoff', default=100)
parser.add_argument('-o','--out', type=str, help='Output file', default=sys.stdout)
parser.add_argument('--full', help='Print full CDS/Proteins only', action='store_true')
args = parser.parse_args()

with open(args.sequences,'r') as seqs:
    for record in SeqIO.parse(seqs,'fasta'):
        if args.full:
            if record.seq[0] != 'M' and record.seq[-1] != 'X':
                continue
        if len(record.seq) >= args.length:
            SeqIO.write(record,args.out,'fasta')
