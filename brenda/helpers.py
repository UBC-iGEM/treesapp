from dataclasses import dataclass
from typing import Optional
from Bio import Entrez
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BrendaData:
    organism: str
    accessions: Optional[list[str]] = None
    tax_ids: Optional[list[str]] = None
    km: Optional[float] = None
    kcat: Optional[float] = None
    catalytic_efficiency: Optional[float] = None
    ph_optima: Optional[float] = None
    ph_range: Optional[tuple[float, float]] = None
    temp_optima: Optional[float] = None
    temp_range: Optional[tuple[float, float]] = None

@dataclass_json
@dataclass
class BrendaEntries:
    entries: dict[str, BrendaData]


Entrez.email = "drylab@ubcigem.com"

class FASTA:
    entries: list[tuple[str, str, str]]

    def __init__(self, fasta: str) -> None:
        self.entries = []
        records = fasta.split('>')
        for record in records:
            if not record.strip():
                continue
            header, *seq = record.split('\n')
            prefix, id = header.split('.', 1)
            prefix = prefix.strip()
            self.entries.append((prefix, id, '\n'.join(seq)))

    def __str__(self) -> str:
        out = ""
        for prefix, id, record in self.entries:
            out += f">{prefix}.{id}\n{record}"
        return out

    def filter(self, valid_entries: set[str]) -> None:
        filtered: list[tuple[str, str, str]] = []
        for prefix, id, record in self.entries:
            if f"{prefix}.{id}" in valid_entries:
                filtered.append((prefix, id, record))
        self.entries = filtered

    def elim_doubles(self) -> None:
        visited = set()
        unique_entries: list[tuple[str, str, str]] = []
        for prefix, id, seq in self.entries:
            sequence = seq.replace(' ', '').replace('\r', '').replace('\n', '')
            if sequence not in visited:
                visited.add(sequence)
                unique_entries.append((prefix, id, seq))

        print(f"Doubling removal eliminated {len(self.entries) - len(unique_entries)} sequences")
        self.entries = unique_entries
