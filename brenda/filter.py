from pathlib import Path
from Bio import Entrez
Entrez.email = "drylab@ubcigem.com"

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

    def validate(self) -> bool:
        return self.validate_tax() and self.validate_identifier()


class TSV:
    entries: list[Entry]

    def __init__(self, tsv: str):
        tsv = tsv.strip()
        lines = tsv.split('\n')
        self.entries = []

        for line in lines:
            parts = line.split('\t')
            assert len(parts) == 2

            (identifier, tax) = (parts[0], parts[1])
            identifier_parts = identifier.split('.')

            (prefix, id) = (identifier_parts[0], str.join("", identifier_parts[1:]))
            self.entries.append(Entry(prefix, id, tax))

    def __str__(self) -> str:
        out = ""
        for item in self.entries:
            out += item.__str__()
        return out

    def valid_sequences(self) -> set[str]:
        out = set()
        for (i, item) in enumerate(self.entries):
            if item.validate():
                out.add(f"{item.prefix}.{item.id}")
            else:
                print(f"Item {i+1} is invalid!")
        return out

class FASTA:
    entries: list[tuple[str, str]]

    def __init__(self, fasta: str) -> None:
        self.entries = []
        records = fasta.split('>')
        for record in records:
            parts = record.split('\n')
            id = parts[0].strip()
            self.entries.append((id, record))

    def __str__(self) -> str:
        out = ""
        for _, record in self.entries:
            out += f">{record}"
        return out

    def filter(self, valid_entries: set[str]) -> "FASTA":
        filtered = []
        for id, record in self.entries:
            if id in valid_entries:
                filtered.append(record)
        return FASTA(">".join(filtered))


if __name__ == "__main__":
    valid_entries: set[str] = set()
    current_path = Path(__file__).parent.resolve()
    with open(current_path / "CAmap.tsv") as tsv_file:
        tsv = tsv_file.read()
        tsv_parsed = TSV(tsv)
        valid_entries = tsv_parsed.valid_sequences()
    with open(current_path / "CAseq.fa") as fasta_file:
        fasta = FASTA(fasta_file.read())
        new_fasta = fasta.filter(valid_entries)
        with open(current_path / "nova.fa", 'w') as out:
            out.write(str(new_fasta))
