from pathlib import Path

from Bio import Entrez
from helpers import FASTA

class Entry:
    prefix: str
    id: str
    tax: str

    def __init__(self, prefix: str, id: str, tax: str) -> None:
        self.prefix = prefix
        self.id = id
        self.tax = tax

    def __str__(self) -> str:
        return f"{self.prefix}.{self.id}\n"

    def validate_tax(self) -> bool:
        return self.tax.strip() != "r__Root"

    def validate_identifier(self) -> bool:
        try:
            with Entrez.esearch(db="protein", term=self.id, retmode="xml") as handle:
                record = Entrez.read(handle)
                return int(record["Count"]) > 0
        except Exception as e:
            print(f"Error validating {self.prefix}.{self.id}: {e}")
            return False

    def validate(self, index: int) -> bool:
        if not self.validate_tax():
            print(f"Tax data for item {index} is missing!")
            return False
        if not self.validate_identifier():
            print(f"ID for item {index} ({self.id}) is missing!")
            return False
        return True


class TSV:
    entries: list[Entry]

    def __init__(self, tsv: str) -> None:
        tsv = tsv.strip()
        lines = tsv.split('\n')
        self.entries = []

        for line in lines:
            parts = line.split('\t')
            assert len(parts) == 2

            (identifier, tax) = (parts[0], parts[1])
            prefix, *rest = identifier.split('.')

            id = '.'.join(rest)
            self.entries.append(Entry(prefix, id, tax))

    def __str__(self) -> str:
        out = ""
        for item in self.entries:
            out += item.__str__()
        return out

    def valid_sequences(self) -> set[str]:
        out = set()
        for (i, item) in enumerate(self.entries):
            if item.validate(i + 1):
                out.add(f"{item.prefix}.{item.id}")
        return out


valid_entries: set[str] = set()
current_path = Path(__file__).parent.resolve()

with open(current_path / "treesapp-inputs/map.tsv") as tsv_file:
    tsv = tsv_file.read()
    tsv_parsed = TSV(tsv)
    valid_entries = tsv_parsed.valid_sequences()

with open(current_path / "treesapp-inputs/seq.fa") as fasta_file:
    fasta = FASTA(fasta_file.read())
    fasta.elim_doubles()
    fasta.filter(valid_entries)
    with open(current_path / "treesapp-outputs/nova.fa", 'w') as out:
        out.write(str(fasta))
