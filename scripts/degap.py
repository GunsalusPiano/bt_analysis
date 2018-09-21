#!/usr/bin/python2.6

import sys
import re
from Bio import AlignIO

if (len(sys.argv) != 3):
  sys.exit("specify: unaligned_sequence_file unaligned_sequence_file_format (output will be fasta-format to stdout)")

alignment = AlignIO.read(open(sys.argv[1]), sys.argv[2])

length=[]

count = 0

for record in alignment :

#	print record.id+'\n'

#	print record.id

	#print record.id

	#if (record.id == "pb2" or record.id == "pa" or record.id == "pb1" or record.id == "ns1" or record.id == "m1/2" or record.id == "Bm1_46455" or record.id == "DS239419"):
	if (record.id == "NA/1-1410"):
		ref = record.seq
		
		#print('>'+record.id+'\n'+record.seq+'\n')
	else:
		out = ''
		for b in range(0,len(record.seq)):
			if (re.match("[a-zA-Z]",ref[b])):
				out = out + record.seq[b]

		print('>'+record.id+'\n'+out)
			

#f = open(sys.argv[1]+".stats",'w')

#print f.write(str(length))
