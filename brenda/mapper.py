from pathlib import Path
from helpers import FASTA, BrendaData, BrendaEntries
from pprint import pprint

self_path = Path(__file__).parent
with open(self_path / "outputs/nova.fa") as f:
    file_contents = f.read()
    fasta_taxes = [ tax for tax, _, _ in FASTA(file_contents).entries ]

with open(self_path / "outputs/brenda_serialized.json") as f:
    file_contents = f.read()
    brenda_data: BrendaEntries = BrendaEntries.from_json(file_contents)
    entries = [ (item.organism, item.catalytic_efficiency) for item in brenda_data.entries if item.catalytic_efficiency ]
    sorted_entries = sorted(entries, key=lambda x: x[1], reverse=True)
    pprint(sorted_entries)
