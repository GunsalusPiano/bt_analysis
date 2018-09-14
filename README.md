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

Also had to omit AL731825 and CP015350 as they were improperly annotated in NCBI.
```shell
# I deleted the specific accessions from the accession file
grep --no-group-separator -A1 -F -f cry-accessions.txt crickmore-cds.1line.fasta  > temp && mv temp crickmore-cds.fasta
```

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
Since there are multiple aa sequences per cds I grabbed the largest with this script
```shell
python ../../../scripts/get-longest-seq.py a1-d12.allseqs.cds.getorf.fasta > a1-d12.allseqs.cds.getorf.largets-aa.fasta
```

now it's a protein-protein blast
```shell
blastp -query a1-d12.allseqs.cds.getorf.largets-aa.fasta -db all-cry-aa.fasta -out a1-d12.allseqs.cds.getorf.blastp.tsv -outfmt '6 qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_threads 4 -max_target_seqs 1 -culling_limit 1 -max_hsps 1 -evalue 0.00005
```

This didn't work out very well - there were an insane amount of hits with no clear cut method to filter out, especially considering the distribution of protein lengths in the crickmore db.

So next I ran blastx (translated query vs protein db) on the PATRIC contigs and it came out looking much better.
```shell
blastx -query a1-d12.contigs.fasta -db all-cry-aa.fasta -out contig-blastx.tsv -outfmt '6 qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_threads 4 -max_target_seqs 2 -culling_limit 1 -evalue 0.00005
```
I think at this point in the game we should just roll with ToxinScanner and come back to this later to see the likelihood of it missing anything.
