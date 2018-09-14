import pandas as pd
import sys
import argparse

parser = argparse.ArgumentParser(description='Provides the means to sort and filter blast results.')
parser.add_argument('-i', '--input', type=str, help='blast file in outfmt 6', required=True)
parser.add_argument('-e', '--evalue', type=float, help='evalue cutoff')
parser.add_argument('-p', '--percend_identity', type=float, help='Percent identity cutoff')
parser.add_argument('-l', '--aln_length', type=int, help='Alignment length cutoff')
parser.add_argument('-c', '--col_head', type=str, help='Column header definitions')
args = parser.parse_args()

# print(args)

df = pd.read_table(args.input, header=None)
#
# cols = ['qaccver', 'saccver', 'pident', 'length', 'qlen', 'slen',
#         'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send',
#         'evalue', 'bitscore']

df.columns = 'qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore'.strip().split(' ')

df_filtered = df[(df['pident'] >= 90.0) & (df['length'] >= 100)]

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_filtered)
