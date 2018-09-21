import pandas as pd
import sys
import argparse
from Bio import SeqIO

parser = argparse.ArgumentParser(description='Provides the means to sort and filter blast results.')
parser.add_argument('-i', '--input', type=str, help='blast file in outfmt 6', required=True)
parser.add_argument('-e', '--evalue', type=float, help='evalue cutoff', default = 0)
parser.add_argument('-p', '--percent_identity', type=float, help='Percent identity cutoff', default = 0)
parser.add_argument('-l', '--aln_length', type=int, help='Alignment length cutoff', default = 0)
parser.add_argument('-c', '--col_head', type=str, help='Column header definitions')
parser.add_argument('-s', '--sequence', type=str, help='Sequence file to extract from', required=True)
args = parser.parse_args()

df = pd.read_table(args.input, header=None)

df.columns = 'qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore'.strip().split(' ')

df_filtered = df[(df['pident'] >= args.percent_identity) & (df['length'] >= args.aln_length)]

with open(args.sequence, 'r') as f:
    for record in SeqIO.parse(f,'fasta'):
        if record.id in df_filtered.qaccver.values:
            hit = df_filtered.loc[ df_filtered['qaccver'] == record.id]
            print(hit)
            start = int(hit.qstart.values)
            end = int(hit.qend.values)
            if start > end:
                start = int(hit.qend.values)
                end = int(hit.qstart.values)
            print(record.seq[start-1:end].translate())
            # print(df_filtered.loc[ df_filtered['qaccver'] == record.id])
