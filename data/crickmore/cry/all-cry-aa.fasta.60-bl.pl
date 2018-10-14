#!/usr/bin/perl
$host = shift;
$instance = shift;
$arg = shift;

#### random sleep, rand() can be a fraction of second
select(undef,undef,undef,rand());

if ($arg) {
  @ids = split(/,/, $arg);
}
else {
  while(1) {
    if (opendir(DDIR, "all-cry-aa.fasta-seq")) { 
      @ids = grep {/^\d+$/} readdir(DDIR);
      last;
    }
    else {
      sleep(1);
    }
  }
}

foreach $id (@ids) {

  next unless (-e "all-cry-aa.fasta-seq/$id");
  next if (-e "all-cry-aa.fasta-seq/$id.lock");
  $cmd = `touch all-cry-aa.fasta-seq/$id.lock`;

  if (50) {
    $cmd = `blastp -outfmt 6 -db ./all-cry-aa.fasta.60 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 1 -query all-cry-aa.fasta-seq/$id -out all-cry-aa.fasta-bl/$id`;
    $cmd =                         `../../../scripts/cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout_multi all-cry-aa.fasta-bl/$id -c 0.45 -ce -1 -aS 0 -aL 0 -G 1 -prog blastp -bs 0 >> all-cry-aa.fasta-blm/$host.$instance`;
  }
  elsif (1) {
    $cmd = `blastp -outfmt 6 -db ./all-cry-aa.fasta.60 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 1 -query all-cry-aa.fasta-seq/$id | ../../../scripts/cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout all-cry-aa.fasta-bl/$id -c 0.45 -ce -1 -aS 0 -aL 0 -G 1 -prog blastp -bs 1`;
  }
  else {
    $cmd = `blastp -outfmt 6 -db ./all-cry-aa.fasta.60 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 1 -query all-cry-aa.fasta-seq/$id -out all-cry-aa.fasta-bl/$id`;
    $cmd =                         `../../../scripts/cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout all-cry-aa.fasta-bl/$id -c 0.45 -ce -1 -aS 0 -aL 0 -G 1 -prog blastp -bs 0`;
  }
  $cmd = `rm -f  all-cry-aa.fasta-seq/$id`;
  $cmd = `rm -f  all-cry-aa.fasta-seq/$id.lock`;
}

($tu, $ts, $cu, $cs) = times();
$tt = $tu + $ts + $cu + $cs;
$cmd = `echo $tt >> all-cry-aa.fasta-seq/host.$host.$instance.cpu`;

