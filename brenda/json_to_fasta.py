from helpers import BrendaEntries

with open("outputs/brenda_serialized.json") as f:
    data_entries: BrendaEntries = BrendaEntries.from_json(f.read())

fasta_lines = map(lambda x: x.fasta or "" if x.catalytic_efficiency is not None else "", data_entries.entries)

with open("outputs/SELE_brenda.fa", "w") as f:
    f.writelines(fasta_lines)
