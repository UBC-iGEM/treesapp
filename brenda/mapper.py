from pathlib import Path
from helpers import FASTA, BrendaEntries

self_path = Path(__file__).parent
with open(self_path / "inputs/COG3338.fasta") as f:
    file_contents = f.read()

fasta_taxes = [ tax for tax, _, _ in FASTA(file_contents).entries ]

with open(self_path / "outputs/brenda_serialized.json") as f:
    brenda_data: BrendaEntries = BrendaEntries.from_json(f.read())

counter = 0
for item in fasta_taxes:
    if item in brenda_data.entries:
        print(f"Found for tax {item}: {brenda_data.entries.get(item)}")
        counter += 1
print(counter)
