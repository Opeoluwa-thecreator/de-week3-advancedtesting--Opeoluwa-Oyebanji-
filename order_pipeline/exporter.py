# order_pipeline/exporter.py
import json
from typing import List, Dict, Any


class Exporter:
    def __init__(self, out_path: str):
        self.out_path = out_path

    def export_cleaned(self, cleaned: List[Dict[str, Any]]) -> None:
        with open(self.out_path, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=2)
