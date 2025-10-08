import pandas as pd
import matplotlib.pyplot as plt

# === Load your files ===
annotree = pd.read_csv("annotree_hits.csv")          # raw hits
with open("ca_positive_ids.txt") as f:               # filtered IDs
    positive_ids = [line.strip() for line in f if line.strip()]
taxonomy = pd.read_csv("ca_with_taxonomy_uniprot.csv")       # final with taxonomy

# === Count entries ===
counts = {
    "AnnoTree Hits": len(annotree),
    "Filtered IDs": len(positive_ids),
    "With Taxonomy": len(taxonomy)
}

print("Counts:", counts)

# === Bar chart ===
plt.figure(figsize=(6, 5))  # Taller figure for more space
bars = plt.bar(counts.keys(), counts.values(),
               color=["#6baed6", "#fd8d3c", "#74c476"])

# Add numbers on top of bars (closer, not hitting title)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1,   # +1 instead of +10
             f"{yval}", ha="center", va="bottom", fontsize=10)

# Adjust y-axis to give extra headroom
plt.ylim(0, max(counts.values()) + 10)

plt.ylabel("Number of sequences")
plt.title("GTDB/NCBI Filtering Workflow for α-CA Sequences")
plt.tight_layout()
plt.savefig("gtdb_filtering_workflow.png", dpi=300)
plt.show()
