# %%
# Imports
from Bio import SeqIO
from Bio.SeqUtils.IsoelectricPoint import IsoelectricPoint as IP

# %%
# Short function to compute isoelectric points
def compute_pis(fasta_path):
    """
    Computes the isoelectric points (pI) of all sequences in a FASTA file.
    """
    results = []
    for record in SeqIO.parse(fasta_path, "fasta"):
        seq = record.seq
        ip = IP(seq)
        results.append((record.id, ip.pi()))
    return results

# %%
# Path to FASTA file (relative to this script)
fasta_path = "../COG3338-outputs/aCACOG3338.fa"

# Compute and print pI values
pis = compute_pis(fasta_path)
for seq_id, pi in pis:
    print(f"{seq_id}: pI = {pi:.2f}")
