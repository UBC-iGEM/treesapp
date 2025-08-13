from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Optional
from numpy import float32, float64

# %% Load DB into memory
from brendapyrser import BRENDA
from helpers import BrendaEntries, BrendaData
brenda = BRENDA("inputs/brenda_db.txt")
ec = "4.2.1.1"
rxn = brenda.reactions.get_by_id(ec)


# %% Collect KM, pH, and temp data
data_entries: dict[str, BrendaData] = { }

for substrate, measurements in rxn.KMvalues.items():
    for entry in measurements:
        km_value = entry.get("value")
        species = entry.get("species", [])
        if not species:
            continue
        organism = species[0].lower()
        entry = data_entries.setdefault(organism, BrendaData(organism))
        entry.km = km_value

for substrate, measurements in rxn.Kcatvalues.items():
    for entry in measurements:
        km_value = entry.get("value")
        species = entry.get("species", [])
        if not species:
            continue
        organism = species[0].lower()
        entry = data_entries.setdefault(organism, BrendaData(organism))
        entry.kcat = km_value

for org, data in data_entries.items():
    entry = data_entries[org]
    if entry.km is not None and entry.kcat is not None:
        entry.catalytic_efficiency = entry.kcat / entry.km

for ph_type in ["optimum", "range"]:
    for entry in rxn.PH.get(ph_type, []):
        value = entry.get("value")
        if value is None:
            continue
        species = entry.get("species", [])
        if not species:
            continue
        organism = species[0].lower()
        entry = data_entries.setdefault(organism, BrendaData(organism))

        if ph_type == "optimum" and isinstance(value, (int, float, float32, float64)):
            entry.ph_optima = float(value)
        elif ph_type == "range" and isinstance(value, list) and len(value) == 2:
            entry.ph_range = (float(value[0]), float(value[1]))


for temp_type in ["optimum", "range"]:
    for entry in rxn.temperature.get(temp_type, []):
        value = entry.get("value")
        if value is None:
            continue
        species = entry.get("species", [])
        if not species:
            continue
        organism = species[0].lower()
        entry = data_entries.setdefault(organism, BrendaData(organism))

        if temp_type == "optimum" and isinstance(value, (int, float, float32, float64)):
            entry.temp_optima = float(value)
        elif temp_type == "range" and isinstance(value, list) and len(value) == 2:
            entry.temp_range = (value[0], value[1])


# %% Add UniProtKB accession data
def get_uniprot_id(organism: str) -> Optional[tuple[str, list[str], list[str]]]:
    import requests
    query = f'ec:{ec} AND (organism_name:"{organism}")'
    params = {
        "query": query,
        "fields": "accession,organism_id",
        "format": "json",
        "size": "1",
    }

    UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"
    for _ in range(1, 5):
        r = requests.get(UNIPROT_SEARCH_URL, params=params, timeout=30)
        r.raise_for_status()
        results = r.json().get("results", [])
        if results:
            accessions, tax_ids = [], []
            for result in results:
                accessions.append(result.get("primaryAccession"))
                tax_ids.append(result.get("organism").get("taxonId"))
            return organism, accessions, tax_ids
        else:
            sleep(0.5)
            continue
    return None

with ThreadPoolExecutor(max_workers=50) as ex:
    for result in ex.map(get_uniprot_id, data_entries.keys()):
        if result is None:
            continue
        organism, acc, tax = result
        data_entries[organism].accessions = acc
        data_entries[organism].tax_ids = tax

final_map = { }
for data in data_entries.values():
        for tax_id in (data.tax_ids or []):
            final_map[tax_id] = data

brenda_data = BrendaEntries(entries=final_map)


# %% Export to JSON
with open("outputs/brenda_serialized.json", "w") as f:
    f.write(brenda_data.to_json(indent=4))
    print(f"Saved {len(brenda_data.entries)} organism-specific entries to 'brenda_serialized.json'")
