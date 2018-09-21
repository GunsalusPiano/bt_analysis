import pandas as pd
import sys
import argparse
from Bio import SeqIO
from tabulate import tabulate

parser = argparse.ArgumentParser(description='Provides the means to sort and filter blast results.')
parser.add_argument('-i', '--input', type=str, help='blast file in outfmt 6', required=True)
parser.add_argument('-e', '--evalue', type=float, help='evalue cutoff', default = 10)
parser.add_argument('-p', '--percent_identity', type=float, help='Percent identity cutoff', default = 0)
parser.add_argument('--qlen', type=int, help='Query sequence length cutoff', default = 0)
parser.add_argument('-l', '--aln_length', type=int, help='Alignment length cutoff', default = 0)
parser.add_argument('-c', '--col_head', type=str, help='Column header definitions')
parser.add_argument('-s', '--sequence', type=str, help='Sequence file to extract from')
parser.add_argument('-q','--qcov', type=float, help='Query coverage cutoff', default = 0)
parser.add_argument('-o','--out', type=str, help='Output file', default=sys.stdout)

args = parser.parse_args()

# print(args)

df = pd.read_table(args.input, header=None)
df.columns = 'qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore'.strip().split(' ')
df['qcov'] = (df['length']/df['qlen'])*100
df_filtered = df[(df['pident'] >= args.percent_identity) & \
              (df['length'] >= args.aln_length) & \
              (df['evalue'] <= args.evalue) & \
              (df['qcov'] >= args.qcov) & \
              (df['qlen'] >= args.qlen)]



if args.sequence:
    with open(args.sequence, 'r') as f:
        seqs = list()
        for record in SeqIO.parse(f,'fasta'):
            if record.id in df_filtered.qaccver.values and \
                record.seq[0] == 'M':
                seqs.append(record)
        SeqIO.write(seqs,args.out,'fasta')

else:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.precision', 2):
        print(tabulate(df_filtered, headers='keys', tablefmt='markdown'))
