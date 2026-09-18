"""
metric_loader.py — loads the structured CSVs and exposes values through
canonical metric names (from metric_registry.json), so the reasoning
engine never touches a raw CSV column name directly.

Usage:
    loader = MetricLoader(data_dir="./data")
    val = loader.get("agricultural_pct", key="IND")       # country-level lookup
    val = loader.get("regional_species_richness", key="Karnataka")  # state-level lookup
"""

import json
import csv
from pathlib import Path
from typing import Optional, Dict


class MetricLoader:
    def __init__(self, data_dir: str, registry_path: str = "metric_registry.json"):
        self.data_dir = Path(data_dir)
        with open(registry_path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)

        # canonical_metric -> (csv_filename, key_column, raw_column)
        self._metric_index: Dict[str, tuple] = {}
        for csv_filename, spec in self.registry.items():
            if csv_filename.startswith("_"):
                continue
            key_col = spec["key_column"]
            for raw_col, canonical in spec["columns"].items():
                self._metric_index[canonical] = (csv_filename, key_col, raw_col)

        self._tables: Dict[str, list] = {}  # cache loaded CSVs

    def _load_table(self, csv_filename: str) -> list:
        if csv_filename not in self._tables:
            path = self.data_dir / csv_filename
            with open(path, newline="", encoding="utf-8") as f:
                self._tables[csv_filename] = list(csv.DictReader(f))
        return self._tables[csv_filename]

    def get(self, canonical_metric: str, key: str) -> Optional[float]:
        """
        Look up a value for a canonical metric name (e.g. 'agricultural_pct')
        by its key (e.g. an iso3 code like 'IND', or a state name like
        'Karnataka' for the regional table). Returns None if not found.
        """
        if canonical_metric not in self._metric_index:
            raise KeyError(
                f"'{canonical_metric}' is not in the metric registry. "
                f"Known metrics: {sorted(self._metric_index)}"
            )

        csv_filename, key_col, raw_col = self._metric_index[canonical_metric]
        table = self._load_table(csv_filename)

        for row in table:
            if row.get(key_col) == key:
                raw_value = row.get(raw_col)
                if raw_value in (None, ""):
                    return None
                try:
                    return float(raw_value)
                except ValueError:
                    return raw_value  # non-numeric field, return as-is

        return None  # key not found in this table

    def available_metrics(self) -> list:
        return sorted(self._metric_index.keys())


if __name__ == "__main__":
    # Example usage — adjust data_dir to wherever your CSVs actually live
    loader = MetricLoader(data_dir=".")
    print("Available metrics:", loader.available_metrics())

    # Example lookups (will print None if the CSVs aren't present in data_dir)
    print("India forest_pct:", loader.get("forest_pct", key="IND"))
    print("Karnataka regional_species_richness:",
          loader.get("regional_species_richness", key="Karnataka"))