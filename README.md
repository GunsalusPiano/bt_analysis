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
I ran blastx with the contigs against the crickmore database. The results were the same as the d12 ToxinScanner results.
```shell
blastx -query a1-d12.contigs.fasta -db all-cry-aa.fasta -out contig-blastx.tsv -outfmt '6 qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_threads 4 -max_target_seqs 1 -culling_limit 1 -evalue 0.00005 -max_hsps 1
```

```
accn|91061.11.con.0048  Cry6Ba1 30.571  350     17299   395     217     6       8651    9622    43      392     2.25e-32        129
accn|91061.11.con.0049  Cry55Aa3        26.855  283     17477   363     180     8       3098    2307    68      342     2.78e-12        68.2
accn|91061.11.con.0054  Cry6Aa1 28.736  348     15326   475     224     5       6907    7878    37      384     8.96e-37        144
accn|91061.11.con.0055  Cry75Aa3        33.784  222     15041   317     128     8       5681    5064    94      312     3.70e-18        85.1
accn|91061.11.con.0060  Cry4Ba2 76.577  111     12780   1136    26      0       6932    7264    1026    1136    7.47e-39        156
accn|91061.11.con.0065  Cry4Ba1 62.742  1138    11299   1136    400     11      6594    9956    5       1135    0.0     1397
accn|91061.11.con.0089  Cry11Bb2        73.755  522     8574    793     90      4       5654    7114    1       510     0.0     691
accn|91061.11.con.0099  Cry44Aa1        41.772  316     4521    686     156     9       4471    3554    373     670     3.03e-57        207
accn|91061.11.con.0110  Cry4Aa2 45.285  1230    4103    1180    532     30      3734    312     1       1178    0.0     950
```

So to get something going I will use the PATRIC predicted genes (which a previous analysis showed there is very good correlation between ToxinScanner and PATRIC for gene finding) and blastp these to get the predicted toxins. I set the minimum alignment length to 100bp and the query coverage at 80% and a minimum sequence lenght of 200bp (this yielded 6 sequences from the d12 sample). These will then be fed directly into an alignment algorithm.

```shell
blastp -query PATRIC_genome_feature.fasta -db all-cry-aa.fasta -out PATRIC_genome_feature.blastp.tsv -outfmt '6 qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_threads 4 -max_target_seqs 3 -max_hsps 2 -culling_limit 2 -evalue 0.00005

python ../../../scripts/filter-blast-results.py -i PATRIC_genome_feature.blastp.tsv  -l 100 -q 80 --qlen 200 -s PATRIC_genome_feature.fasta -o PATRIC_genome_feature.blastp.filtered.fasta
```
```
qaccver                 saccver      pident    length    qlen    slen    mismatch    gapopen    qstart    qend    sstart    send    evalue    bitscore      qcov
--  ----------------------  ---------  --------  --------  ------  ------  ----------  ---------  --------  ------  --------  ------  --------  ----------  --------
0  fig|91061.11.peg.3383|  Cry6Ba1      30.571       350     353     395         217          6        19     342        43     392  2.02e-43       150     99.1501
1  fig|91061.11.peg.3383|  Cry6Aa1      27.586       348     353     475         228          5        19     342        37     384  9.42e-40       142     98.5836
2  fig|91061.11.peg.3393|  Cry55Aa3     26.855       283     324     363         180          8        57     320        68     342  4.55e-18        80.1   87.3457
3  fig|91061.11.peg.3393|  Cry55Aa2     26.502       283     324     362         181          8        57     320        68     342  7.84e-18        79.3   87.3457
4  fig|91061.11.peg.3619|  Cry6Aa2      28.736       348     353     475         224          5        19     342        37     384  1.68e-44       155     98.5836
5  fig|91061.11.peg.3619|  Cry6Aa1      28.736       348     353     475         224          5        19     342        37     384  1.68e-44       155     98.5836
17  fig|91061.11.peg.3789|  Cry19Ca1     55.199      1183    1167    1192         474         19         5    1160         6    1159  0             1229    101.371
18  fig|91061.11.peg.3789|  Cry4Aa2      49.002      1202    1167    1180         512         31         5    1134         6    1178  0             1031    102.999
19  fig|91061.11.peg.3792|  Cry4Ba5      62.742      1138    1146    1136         400         11        25    1145         5    1135  0             1397     99.3019
20  fig|91061.11.peg.3792|  Cry4Ba1      62.742      1138    1146    1136         400         11        25    1145         5    1135  0             1397     99.3019
33  fig|91061.11.peg.4097|  Cry44Aa1     44.286       280     286     686         140          8        17     286       373     646  7e-62          203     97.9021
35  fig|91061.11.peg.4331|  Cry4Aa3      45.285      1230    1218    1180         532         30         1    1141         1    1178  0              949    100.985
36  fig|91061.11.peg.4331|  Cry4Aa2      45.285      1230    1218    1180         532         30         1    1141         1    1178  0              949    100.985
```

So now to see if these are full length ORFs I will extract just those contigs that hit and see if they are full length.
```shell
python ../../../scripts/get-seq-by-names.py -s a1-d12.contigs.fasta -n accn\|91061.11.con.0048 accn\|91061.11.con.0049 accn\|91061.11.con.0054 accn\|91061.11.con.0055 accn\|91061.11.con.0060 accn\|91061.11.con.0065 accn\|91061.11.con.0089 accn\|91061.11.con.0099 accn\|91061.11.con.0110

mv out.fasta toxin-contigs.fasta

getorf -find 1 -sequence toxin-contigs.fasta -out toxin-contigs.getorf.fasta

blastp -query toxin-contigs.getorf.fasta -db all-cry-aa.fasta -out test.tsv -outfmt '6 qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_threads 4 -max_target_seqs 2 -culling_limit 1 -evalue 0.00005
```
So this is not quite what I was expecting. This is a very basic
```
EMBOSS_009_52	Cry4Aa2	45.285	1230	1218	1180	532	30	1	1141	1	1178	0.0	949
EMBOSS_006_153	Cry19Ca1	55.199	1183	1167	1192	474	19	5	1160	6	1159	0.0	1229
EMBOSS_006_65	Cry4Ba1	62.742	1138	1188	1136	400	11	67	1187	5	1135	0.0	1397
EMBOSS_001_65	Cry6Ba1	30.571	350	353	395	217	6	19	342	43	392	2.02e-43	150
EMBOSS_003_56	Cry6Aa1	28.736	348	353	475	224	5	19	342	37	384	1.68e-44	155
EMBOSS_002_210	Cry55Aa3	26.855	283	324	363	180	8	57	320	68	342	4.55e-18	80.1
EMBOSS_008_38	Cry44Aa1	44.245	278	269	686	139	8	2	269	375	646	8.78e-62	202
EMBOSS_004_157	Cry75Aa2	34.404	218	294	317	124	8	92	293	98	312	7.94e-24	95.1
EMBOSS_005_178	Cry73Aa1	34.884	215	469	802	117	7	270	469	595	801	9.11e-25	103
EMBOSS_007_85	Cry8Pa3	53.642	151	184	173	70	0	33	183	21	171	1.19e-59	180
EMBOSS_005_124	Cry75Aa3	35.714	126	345	317	80	1	111	236	95	219	4.69e-16	73.9
EMBOSS_005_56	Cry4Ba2	76.577	111	119	1136	26	0	9	119	1026	1136	1.04e-55	182
EMBOSS_007_47	Cry11Bb2	90.141	71	71	793	7	0	1	71	440	510	3.14e-40	135
EMBOSS_005_52	Cry11Bb2	91.045	67	136	793	6	0	70	136	726	792	2.01e-35	125
EMBOSS_007_51	Cry11Bb1	86.441	59	59	750	8	0	1	59	564	622	4.81e-29	102
EMBOSS_005_26	Cry4Ba2	69.643	56	71	1136	17	0	10	65	1064	1119	5.08e-23	86.7
EMBOSS_007_37	Cry11Bb2	95.556	45	45	793	2	0	1	45	129	173	3.13e-26	94.4
EMBOSS_009_52	Cry11Ba1	64.103	39	1218	724	14	0	1180	1218	682	720	4.99e-11	62.8
EMBOSS_007_34	Cry11Bb1	89.474	38	40	750	4	0	3	40	1	38	3.42e-17	68.2
EMBOSS_007_42	Cry11Bb1	80.952	21	21	750	4	0	1	21	277	297	9.86e-07	37.4
EMBOSS_007_39	Cry11Ba1	100.000	17	17	724	0	0	1	17	224	240	1.03e-08	42.7
```


I also ran blastp after extracting the predicted genes from PATRIC, getting the ORFs, and translating them. This is more of an assessment of PATRIC and ToxinScanner to see if/what is wasn't found by the analysis.
```shell
getorf -noreverse -find 1 -sequence a1-d12.allseqs.cds.fasta -outseq a1-d12.allseqs.cds.getorf.fasta

python ../../../scripts/get-longest-seq.py a1-d12.allseqs.cds.getorf.fasta > a1-d12.allseqs.cds.getorf.largets-aa.fasta

blastp -query a1-d12.allseqs.cds.getorf.largets-aa.fasta -db all-cry-aa.fasta -out a1-d12.allseqs.cds.getorf.blastp.tsv -outfmt '6 qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_threads 4 -max_target_seqs 2 -culling_limit 1 -evalue 0.00005
```
| Gene name | Cry name| percend_identity | aln len | gene len | cry len | mismatch | gapopen | qstart | qend | sstart send | evalue | bitscore |
| 91061.11.peg.3383 | Cry6Ba1 | 30.571 | 350 | 353 | 395 | 217 | 6 | 19 | 342 | 43 | 392 | 2.02e-43 | 150 |
| 91061.11.peg.3393 | Cry55Aa3 | 26.855 | 283 | 324 | 363 | 180 | 8 | 57 | 320 | 68 | 342 | 4.55e-18 | 80.1 |
| 91061.11.peg.3619 | Cry6Aa1 | 28.736 | 348 | 353 | 475 | 224 | 5 | 19 | 342 | 37 | 384 | 1.68e-44 | 155 |
| 91061.11.peg.3631 | Cry75Aa2 | 34.404 | 218 | 294 | 317 | 124 | 8 | 92 | 293 | 98 | 312 | 7.94e-24 | 95.1 |
| 91061.11.peg.3727 | Cry4Ba2 | 69.643 | 56 | 71 | 1136 | 17 | 0 | 10 | 65 | 1064 | 1119 | 5.08e-23 | 86.7 |
| 91061.11.peg.3724 | Cry73Aa1 | 34.884 | 215 | 469 | 802 | 117 | 7 | 270 | 469 | 595 | 801 | 9.11e-25 | 103 |
| 91061.11.peg.3731 | Cry11Bb2 | 91.045 | 67 | 136 | 793 | 6 | 0 | 70 | 136 | 726 | 792 | 2.01e-35 | 125 |
| 91061.11.peg.3734 | Cry75Aa3 | 35.714 | 126 | 345 | 317 | 80 | 1 | 111 | 236 | 95 | 219 | 4.69e-16 | 73.9 |
| 91061.11.peg.3789 | Cry19Ca1 | 55.199 | 1183 | 1167 | 1192 | 474 | 19 | 5 | 1160 | 6 | 1159 | 0.0 | 1229 |
| 91061.11.peg.3792 | Cry4Ba1 | 62.742 | 1138 | 1146 | 1136 | 400 | 11 | 25 | 1145 | 5 | 1135 | 0.0 | 1397 |
| 91061.11.peg.4021 | Cry8Pa3 | 53.642 | 151 | 184 | 173 | 70 | 0 | 33 | 183 | 21 | 171 | 1.19e-59 | 180 |
| 91061.11.peg.4022 | Cry11Bb1 | 89.474 | 38 | 38 | 750 | 4 | 0 | 1 | 38 | 1 | 38 | 7.52e-17 | 67.0 |
| 91061.11.peg.4023 | Cry11Bb2 | 95.556 | 45 | 45 | 793 | 2 | 0 | 1 | 45 | 129 | 173 | 3.13e-26 | 94.4 |
| 91061.11.peg.4024 | Cry11Bb1 | 80.952 | 21 | 21 | 750 | 4 | 0 | 1 | 21 | 277 | 297 | 9.86e-07 | 37.4 |
| 91061.11.peg.4025 | Cry11Bb2 | 90.141 | 71 | 71 | 793 | 7 | 0 | 1 | 71 | 440 | 510 | 3.14e-40 | 135 |
| 91061.11.peg.4033 | Cry73Aa1 | 26.804 | 97 | 179 | 802 | 58 | 4 | 21 | 104 | 190 | 286 | 3.10e-05 | 39.7 |
| 91061.11.peg.4097 | Cry44Aa1 | 44.245 | 278 | 269 | 686 | 139 | 8 | 2 | 269 | 375 | 646 | 8.78e-62 | 202 |
| 91061.11.peg.4331 | Cry4Aa2 | 45.285 | 1230 | 1218 | 1180 | 532 | 30 | 1 | 1141 | 1 | 1178 | 0.0 | 949 |
| 91061.11.peg.4331 | Cry11Ba1 | 64.103 | 39 | 1218 | 724 | 14 | 0 | 1180 | 1218 | 682 | 720 | 4.99e-11 | 62.8 |
| 91061.11.peg.4358 | Cry8La1 | 25.882 | 170 | 540 | 1197 | 103 | 5 | 83 | 240 | 57 | 215 | 9.58e-06 | 44.3 |





# Old stuff
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
