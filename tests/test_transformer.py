# tests/test_transformer.py
import pytest
from order_pipeline.transformer import Transformer, parse_price, parse_quantity, normalize_payment_status

def test_parse_price_variants():
    assert parse_price("$15.99") == pytest.approx(15.99)
    assert parse_price("15.50") == pytest.approx(15.50)
    assert parse_price("N2000") == pytest.approx(2000.0)
    assert parse_price("45 dollars") == pytest.approx(45.0)
    assert parse_price(3) == pytest.approx(3.0)
    assert parse_price("5usd") == pytest.approx(5.0)

def test_parse_quantity_variants():
    assert parse_quantity("2") == 2
    assert parse_quantity(3) == 3
    assert parse_quantity("2pcs") == 2
    assert parse_quantity("N/A") is None

def test_normalize_payment_status():
    assert normalize_payment_status("PAID") == "paid"
    assert normalize_payment_status("Paid") == "paid"
    assert normalize_payment_status("REFUND") == "refunded"
    assert normalize_payment_status("pending") == "pending"

def test_transform_pipeline_with_sample():
    rows = [
        {"order_id": "A", "timestamp": "t", "item": "phone", "quantity": "2", "price": "$10", "payment_status": "Paid"},
        {"order_id": "B", "timestamp": "t", "item": "case", "quantity": "N/A", "price": "$5", "payment_status": "Paid"},
        {"order_id": "C", "timestamp": "t", "item": "cable", "quantity": 1, "price": "N200", "payment_status": "pending"}
    ]
    t = Transformer()
    cleaned = t.transform(rows)
    # first and last should be kept, second should be skipped due to qty parse fail
    assert any(r["order_id"] == "A" for r in cleaned)
    assert any(r["order_id"] == "C" for r in cleaned)
    assert not any(r["order_id"] == "B" for r in cleaned)
    # totals computed
    a = next(r for r in cleaned if r["order_id"] == "A")
    assert a["total"] == 2 * 10.0
