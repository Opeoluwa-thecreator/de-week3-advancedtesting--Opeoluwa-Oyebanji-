# tests/test_analyzer_exporter_pipeline.py
import json
from order_pipeline.analyzer import Analyzer
from order_pipeline.exporter import Exporter
from order_pipeline.pipeline import Pipeline
import tempfile
import os

def test_analyzer_counts_and_totals():
    cleaned = [
        {"order_id": "A", "total": 10.0, "payment_status": "paid"},
        {"order_id": "B", "total": 5.0, "payment_status": "pending"},
        {"order_id": "C", "total": 20.0, "payment_status": "paid"},
        {"order_id": "D", "total": 7.5, "payment_status": "refunded"},
    ]
    a = Analyzer()
    stats = a.compute(cleaned)
    assert stats["total_revenue"] == 30.0  # sum of paid (10 + 20)
    assert stats["counts"]["paid"] == 2
    assert stats["counts"]["pending"] == 1
    assert stats["counts"]["refunded"] == 1
    assert stats["average_revenue"] == round((10+5+20+7.5)/4, 2)

def test_exporter_writes(tmp_path):
    cleaned = [{"order_id": "X", "total": 1.0, "payment_status": "paid"}]
    out = tmp_path / "out.json"
    e = Exporter(str(out))
    e.export_cleaned(cleaned)
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert data[0]["order_id"] == "X"

def test_pipeline_runs_and_writes(tmp_path):
    # use the provided shoplink.json stored at repo root
    sample = os.path.join(os.getcwd(), "shoplink.json")
    out = tmp_path / "cleaned.json"
    p = Pipeline(sample, str(out))
    result = p.run()
    # result contains counts and stats
    assert "raw" in result and result["raw"] > 0
    assert "cleaned" in result
    # file should exist
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    # cleaned should be a list
    assert isinstance(data, list)
