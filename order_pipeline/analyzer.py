# order_pipeline/analyzer.py
from typing import List, Dict, Any


class Analyzer:

    def compute(self, cleaned: List[Dict[str, Any]]) -> Dict[str, Any]:
        totals = [r["total"] for r in cleaned if isinstance(r.get("total"), (int, float))]
        # total revenue -> sum of totals for paid only
        paid_totals = [r["total"] for r in cleaned if r.get("payment_status") == "paid"]
        total_revenue = round(sum(paid_totals), 2)
        avg_revenue = round((sum(totals) / len(totals)) if totals else 0.0, 2)
        counts = {"paid": 0, "pending": 0, "refunded": 0}
        for r in cleaned:
            st = r.get("payment_status")
            if st in counts:
                counts[st] += 1
        return {
            "total_revenue": total_revenue,
            "average_revenue": avg_revenue,
            "counts": counts,
            "total_orders": len(cleaned)
        }
