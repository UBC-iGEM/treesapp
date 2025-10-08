import pandas as pd
import requests
from time import sleep
from concurrent.futures import ThreadPoolExecutor

input_ids_file = "ca_positive_ids.txt"
metadata_file = "bac120_metadata_r226.tsv"
taxonomy_file = "bac120_taxonomy_r226.tsv"
output_file = "ca_with_taxonomy_uniprot.csv"

with open(input_ids_file) as f:
    ids = [line.strip() for line in f if line.strip()]

metadata_df = pd.read_csv(metadata_file, sep="\t")
taxonomy_df = pd.read_csv(taxonomy_file, sep="\t", names=["accession", "taxonomy"])


merged = pd.merge(metadata_df, taxonomy_df, on="accession", how="inner")

filtered = merged[merged["accession"].isin(ids)].copy()

if "ncbi_taxid" not in filtered.columns:
    raise KeyError("No 'ncbi_taxid' column in metadata — check your GTDB metadata file.")

EC_NUMBER = "4.2.1.1"  
UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"

def get_uniprot_by_taxid(ncbi_taxid: int):
    """Query UniProt by NCBI TaxID + EC number, return accessions and tax IDs."""
    if pd.isna(ncbi_taxid):
        return None, None
    query = f"ec:{EC_NUMBER} AND organism_id:{int(ncbi_taxid)}"
    params = {
        "query": query,
        "fields": "accession,organism_id",
        "format": "json",
        "size": "5",
    }
    for _ in range(3):  
        try:
            r = requests.get(UNIPROT_SEARCH_URL, params=params, timeout=30)
            r.raise_for_status()
            results = r.json().get("results", [])
            if results:
                accs = [res.get("primaryAccession") for res in results]
                tax_ids = [res["organism"]["taxonId"] for res in results]
                return ",".join(accs), ",".join(map(str, tax_ids))
        except Exception:
            sleep(0.5)
            continue
    return None, None

with ThreadPoolExecutor(max_workers=25) as ex:
    results = list(ex.map(get_uniprot_by_taxid, filtered["ncbi_taxid"]))

filtered["uniprot_accessions"], filtered["uniprot_tax_ids"] = zip(*results)

def fetch_fasta(accession: str):
    """Fetch UniProt FASTA sequence for first accession (skip header)."""
    if not accession:
        return None
    first_acc = accession.split(",")[0]  
    url = f"https://rest.uniprot.org/uniprotkb/{first_acc}.fasta"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        lines = r.text.strip().split("\n")
        return "".join(lines[1:]) 
    except Exception:
        return None

filtered["uniprot_sequence"] = [
    fetch_fasta(acc) if acc else None
    for acc in filtered["uniprot_accessions"]
]

filtered.to_csv(output_file, index=False)
print(f"Saved {len(filtered)} records with UniProt accessions + sequences to {output_file}")
