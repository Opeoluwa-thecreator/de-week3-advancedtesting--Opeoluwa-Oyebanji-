# tests/test_validator.py
import pytest
from order_pipeline.validator import Validator

VALID_ROW = {
    "order_id": "ORDX",
    "timestamp": "2025-10-19T00:00:00Z",
    "item": "Widget",
    "quantity": 1,
    "price": "$10",
    "payment_status": "paid"
}

MISSING_ROW = {
    "order_id": "ORDY",
    "timestamp": "2025-10-19T00:00:00Z",
    # item missing
    "quantity": 1,
    "price": "$10",
    "payment_status": "paid"
}

def test_validate_accepts_valid():
    v = Validator()
    out = v.validate([VALID_ROW])
    assert len(out) == 1

def test_validate_rejects_missing():
    v = Validator()
    out = v.validate([MISSING_ROW])
    assert len(out) == 0
