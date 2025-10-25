# tests/test_reader.py
import pytest
from order_pipeline.reader import Reader
import json
import os

DATA = "shoplink.json"  

def test_read_json(tmp_path):
    # copy sample to tmp and read
    p = tmp_path / "data.json"
    p.write_text(open(DATA, "r", encoding="utf-8").read(), encoding="utf-8")
    r = Reader(str(p))
    rows = list(r.read())
    assert isinstance(rows, list)
    assert len(rows) > 0

def test_unsupported_format_raises(tmp_path):
    p = tmp_path / "data.txt"
    p.write_text("[]")
    r = Reader(str(p), fmt="csv")
    with pytest.raises(ValueError):
        list(r.read())
