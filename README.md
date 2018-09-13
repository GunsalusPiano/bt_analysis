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

### Crickmore
To obtain known cry sequences I used the Crickmore database to grab the accessions for each gene. I provided all of these to entrez batch to querying against the protein database. Then for those that were not found in the protein database, I provided those accessions to the nucleotide database and grabbed the CDS. Of all the crickmore sequences only 12 were not found:

The following records can't be retrieved:
Id=KJ28844:	nuccore: Wrong UID KJ28844
Id=KJ28845:	nuccore: Wrong UID KJ28845
Id=KJ28846:	nuccore: Wrong UID KJ28846
Id=MG674828:	nuccore: Wrong UID MG674828
Id=MG983752:	nuccore: Wrong UID MG983752
Id=MG983753:	nuccore: Wrong UID MG983753
Id=MG983754:	nuccore: Wrong UID MG983754
Id=MH253686:	nuccore: Wrong UID MH253686
Id=MH475904:	nuccore: Wrong UID MH475904
Id=MH475905:	nuccore: Wrong UID MH475905
Id=MH475906:	nuccore: Wrong UID MH475906
Id=MH475907:	nuccore: Wrong UID MH475907

For the CDS I used transeq (EMBOSS) to translate the first frame:
```shell
transeq -clean -sequence crickmore-cds.fasta -outseq crickmore-cds.translated.fasta -frame 1
```

and then combined them with the aa sequences
```shell
cat crickmore-aa.fasta crickmore-cds.translated.fasta > all-cry-aa.fasta
```

### PATRIC
Now extract the orfs from the Patric assembly

I grabbed the "CDS" from PATRIC. It doesn't look like all of them are only CDS so I'm a little unsure how to proceed with these data.

To proceed, I used getorf to grab all potential CDS between start and stop codons and rendered the amino acid sequences. Since there are multiple per sequence I will grab the longest for now. ** I will need to validate this, maybe just blasting those that are not blatantly CDS **

```shell
getorf -noreverse -find 1 -sequence a1-d12.allseqs.cds.fasta -outseq a1-d12.allseqs.cds.getorf.fasta
```

The shortest sequence from Patric in 63bp so not sure if running `getorf` will be a good move since we might wipe some of the data, but worst case scenario we just omit this step. This analysis will at least catch the low hanging fruit.
```shell
getorf -minsize 230 -noreverse -find 3 -sequence data/patric/a1-d12.allseqs.cds.fasta -outseq data/patric/a1-d12.allseqs.cds.getorf.fasta
grep -c '>' data/patric/a1-d12.allseqs.cds*                                                                            
data/patric/a1-d12.allseqs.cds.fasta:6707
data/patric/a1-d12.allseqs.cds.getorf.fasta:5485
```


I figured tblastx would be the most ideal but the results didn't yield that different of results. So I ran a blastn:
```shell
blastn -db data/crickmore/cry-proteins.cds.getorf.fasta -query data/patric/a1-d12.allseqs.cds.getorf.fasta -max_target_seqs 1 -culling_limit 1 -evalue 0.00005 -out data/patric/a1-d12.allseqs.cds.getorf.blastn.tsv -outfmt '6 qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_threads 4 -max_hsps 1
```
