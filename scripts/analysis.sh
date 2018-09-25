# run from data/patric directory
# scripts = "/Users/alan/projects/gunsiano/bt_analysis/scripts"
# for i in a24 j1 my46 mb11 s1
for i in d12
 do
  blastp -query  $i/PATRIC_genome_feature.fasta -db ../crickmore/cry/all-cry-aa.fasta -out $i/PATRIC_genome_feature.blastp.tsv -outfmt '6 qaccver saccver pident length qlen slen mismatch gapopen qstart qend sstart send evalue bitscore' -num_threads 4 -max_target_seqs 3 -max_hsps 2 -culling_limit 2 -evalue 0.00005

  python3 /Users/alan/projects/gunsiano/bt_analysis/scripts/filter-blast-results.py -i $i/PATRIC_genome_feature.blastp.tsv  -l 100 -q 80 --qlen 200 -s $i/PATRIC_genome_feature.fasta -o $i/PATRIC_genome_feature.blastp.filtered.fasta

done
