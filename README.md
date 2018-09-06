# BT Analysis

The goal here is to:

-   Extract the full lengths cds
    -   Applying this to both the Crickmore database as well as the Patric data seems to make the most sense going forward - things will just be easier.
-   Check to see if there Patric sequences are full length CDS when compared to
    the Crickmore database. This will be done using blast at the nt/prot level.
    -   If yes then proceed as normal.
    -   If no then try to build out the assembly for each contig.
-   Create a tree showing divergence with the nucleotide sequences of each
    Patric cry protein amongst those registered in the Crickmore db.
-   Analyze the protein domains
    -   Need more details about this analysis

## Get Full Length CDS

checking the size of the crickmore sequences I pulled
the shortest was 23bp (wtf) so I think 230bp will be a reasonable cutoff

```shell
get-len.pl cry-proteins.cds.fasta | cut -f2 | sort | uniq -c |  perl -pe 's/^ +//g' | sort -bh -k 2 -t ' ' | head                                                                                                                                       ⏎
1 23
1 99
1 234
1 237
1 302
1 328
5 357
4 369
1 378
1 393
```

To get the ORFS from the crickmore database to make things clearer when aligning

```shell
getorf -minsize 230 -find 3 -noreverse -sequence crickmore_cry_cyt.nucl.fasta -outseq crickmore_cry_cyt.nucl.getorf.fasta
```

After extracting the cds I checked the size of the files. It seems like we can be a bit more stringent with this but I doubt that this will have much of an impact when running blast assuming we set the filters accordingly

```shell
grep -c '>' crickmore_cry_cyt.nucl.*
crickmore_cry_cyt.nucl.fasta:785
crickmore_cry_cyt.nucl.getorf.fasta:4377
```

Make a blast db

```shell
makeblastdb -dbtype nucl -in crickmore_cry_cyt.nucl.getorf.fasta
```

Now extract the orfs from the Patric assembly

```shell
get-len.pl Bacilli_a1-d12.feature_dna.fasta | cut -f2 | sort | uniq -c |  perl -pe 's/^ +//g' | sort -bh -k 2 -t ' ' | head
4 63
1 66
1 69
1 71
3 72
3 73
5 74
5 75
7 76
3 77
```

The shortest sequence from Patric in 63bp so not sure if running `getorf` will be a good move since we might wipe some of the data, but worst case scenario we just omit this step. This analysis will at least catch the low hanging fruit.
