# Data extraction from `all_raw_trees_and_algs.tsv`
> Source: EggNOG v6.0

## extract-msa (og)
> Extract the MSA for all proteins inside the `$og` orthologous group
```bash
rg -P "^$og\t" e6.all_raw_trees_and_algs.tsv \
  | cut -f4 \
  | base64 -d \
  | gunzip -c \
  > $og.msa.fasta
```

## compress
> Compress MSA files with XZ
```sh
xz -k -9 COG3338.msa.fasta KOG0382.msa.fasta
```

## decompress
> Decompress XZ-compressed files
```sh
unxz COG3338.msa.fasta.xz KOG0382.msa.fasta.xz
```

## ungap (file_stub)
> Ungap MSAs
```sh
seqmagick convert $file_stub.msa.fasta $file_stub.fasta --ungap --prune-empty
```

## filter
> Cluster sequences by identity
```sh
mask ungap KOG0382
cd-hit -i KOG0382.fasta -o KOG0382-filtered.fasta -c 0.9 -n 5
```
