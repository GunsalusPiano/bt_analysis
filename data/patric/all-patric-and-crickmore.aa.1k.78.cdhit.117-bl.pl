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
    if (opendir(DDIR, "all-patric-and-crickmore.aa.1k.78.cdhit-seq")) { 
      @ids = grep {/^\d+$/} readdir(DDIR);
      last;
    }
    else {
      sleep(1);
    }
  }
}

foreach $id (@ids) {

  next unless (-e "all-patric-and-crickmore.aa.1k.78.cdhit-seq/$id");
  next if (-e "all-patric-and-crickmore.aa.1k.78.cdhit-seq/$id.lock");
  $cmd = `touch all-patric-and-crickmore.aa.1k.78.cdhit-seq/$id.lock`;

  if (50) {
    $cmd = `blastp -outfmt 6 -db ./all-patric-and-crickmore.aa.1k.78.cdhit.117 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 1 -query all-patric-and-crickmore.aa.1k.78.cdhit-seq/$id -out all-patric-and-crickmore.aa.1k.78.cdhit-bl/$id`;
    $cmd =                         `../../scripts/cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout_multi all-patric-and-crickmore.aa.1k.78.cdhit-bl/$id -c 0.45 -ce -1 -aS 0 -aL 0 -G 1 -prog blastp -bs 0 >> all-patric-and-crickmore.aa.1k.78.cdhit-blm/$host.$instance`;
  }
  elsif (1) {
    $cmd = `blastp -outfmt 6 -db ./all-patric-and-crickmore.aa.1k.78.cdhit.117 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 1 -query all-patric-and-crickmore.aa.1k.78.cdhit-seq/$id | ../../scripts/cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout all-patric-and-crickmore.aa.1k.78.cdhit-bl/$id -c 0.45 -ce -1 -aS 0 -aL 0 -G 1 -prog blastp -bs 1`;
  }
  else {
    $cmd = `blastp -outfmt 6 -db ./all-patric-and-crickmore.aa.1k.78.cdhit.117 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 1 -query all-patric-and-crickmore.aa.1k.78.cdhit-seq/$id -out all-patric-and-crickmore.aa.1k.78.cdhit-bl/$id`;
    $cmd =                         `../../scripts/cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout all-patric-and-crickmore.aa.1k.78.cdhit-bl/$id -c 0.45 -ce -1 -aS 0 -aL 0 -G 1 -prog blastp -bs 0`;
  }
  $cmd = `rm -f  all-patric-and-crickmore.aa.1k.78.cdhit-seq/$id`;
  $cmd = `rm -f  all-patric-and-crickmore.aa.1k.78.cdhit-seq/$id.lock`;
}

($tu, $ts, $cu, $cs) = times();
$tt = $tu + $ts + $cu + $cs;
$cmd = `echo $tt >> all-patric-and-crickmore.aa.1k.78.cdhit-seq/host.$host.$instance.cpu`;

