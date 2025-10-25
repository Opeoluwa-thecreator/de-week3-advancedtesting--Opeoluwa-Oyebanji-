# order_pipeline/validator.py
from typing import Dict, Any, Iterable, List, Optional
import logging

logger = logging.getLogger(__name__)


class Validator:
    REQUIRED = ["order_id", "timestamp", "item", "quantity", "price", "payment_status"]

    def __init__(self, min_quantity: float = 0.0, min_price: float = 0.0):
        self.min_quantity = min_quantity
        self.min_price = min_price

    def _coerce_number(self, v: Any) -> Optional[float]:
        # Accept int/float or numeric strings like "1", "2.5"
        if v is None or v == "":
            return None
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return float(v)
        if isinstance(v, str):
            s = v.strip()
            # try a simple numeric parse
            try:
                return float(s)
            except ValueError:
                return None
        return None

    def validate_one(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not isinstance(row, dict):
            logger.debug("Not a dict: %s", row)
            return None
        # required fields
        for field in self.REQUIRED:
            if field not in row:
                logger.info("Missing required field: %s", field)
                return None
        # quantity and price must be present (strings allowed for now)
        q = row.get("quantity")
        p = row.get("price")
        t = row.get("total", None)  # total optional, will be recalculated later

        # crude checks: must not be null
        if q in (None, "") or p in (None, ""):
            logger.info("Missing numeric fields q/p in row: %s", row.get("order_id"))
            return None

        # we keep the row for transformer to try harder parsing
        return row

    def validate(self, rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out = []
        for r in rows:
            v = self.validate_one(r)
            if v:
                out.append(v)
        return out
