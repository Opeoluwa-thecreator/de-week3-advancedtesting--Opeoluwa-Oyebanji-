# order_pipeline/pipeline.py
from .reader import Reader
from .validator import Validator
from .transformer import Transformer
from .analyzer import Analyzer
from .exporter import Exporter
from typing import Dict, Any


class Pipeline:
    def __init__(self, input_path: str, output_path: str):
        self.reader = Reader(input_path)
        self.validator = Validator()
        self.transformer = Transformer()
        self.analyzer = Analyzer()
        self.exporter = Exporter(output_path)

    def run(self) -> Dict[str, Any]:
        raw = list(self.reader.read())
        valid = self.validator.validate(raw)
        cleaned = self.transformer.transform(valid)
        stats = self.analyzer.compute(cleaned)
        self.exporter.export_cleaned(cleaned)
        return {"raw": len(raw), "valid": len(valid), "cleaned": len(cleaned), **stats}
