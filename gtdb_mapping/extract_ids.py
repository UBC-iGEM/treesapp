# extract_alpha_ca_ids.py
import pandas as pd

# Input and output files
input_csv = "annotree_hits.csv"
output_txt = "ca_positive_ids.txt"

# KEGG ID for alpha-carbonic anhydrase
TARGET_KO = "K01672"

# Read your AnnoTree CSV
df = pd.read_csv(input_csv)

# Filter only alpha CA hits
alpha_df = df[df["keggId"] == TARGET_KO]

# Get unique GTDB IDs
ids = alpha_df["gtdbId"].dropna().unique()

# Save to txt (one per line)
with open(output_txt, "w") as f:
    for id_ in ids:
        f.write(id_ + "\n")

print(f"Saved {len(ids)} alpha CA IDs to {output_txt}")
