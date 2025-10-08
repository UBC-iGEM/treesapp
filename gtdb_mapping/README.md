# Alpha Carbonic Anhydrase Genome Mapping

## Overview
This project maps NCBI genome accession IDs of **alpha carbonic anhydrases (α-CA)** to rich taxonomic and genome metadata from GTDB.

## Data Source
The α-CA genome hits were identified using **[Annotree](https://annotree.uwaterloo.ca/)** by searching for genomes containing the alpha carbonic anhydrase (CA) KEGG Orthology (KO) term.

## Steps Taken
1. Queried Annotree for alpha carbonic anhydrase (α-CA) using the CA KEGG Orthology term.
2. Exported matching **accession IDs** and associated taxonomic data from Annotree.
3. Retrieved additional genome metadata from GTDB, including:
   - Taxonomic ranks (GTDB & NCBI)
   - Assembly details (BioProject, BioSample, country, submitter, date)
   - Genome quality metrics (completeness, contamination, genome size, GC%, etc.)
4. Combined all data into `ca_with_taxonomy.csv`.

## Output
- **File:** `ca_with_taxonomy.csv`
- **Records:** 42 α-CA genomes
- **Columns include:**
  - Accession ID
  - GTDB taxonomy
  - NCBI taxonomy
  - Genome quality metrics
  - Assembly metadata
