from typing import Dict, Any, List

class MaterialAnalyzer:
    """
    Analyzes material inventory, stockout risks, and procurement delays.
    """
    def analyze(self, material_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        total = len(material_data)
        if total == 0:
            return {"material_risk": 15.0, "low_stock_count": 0, "status": "NO_MATERIAL_DATA"}

        low_stock = sum(1 for m in material_data if m.get("quantity", 0) <= m.get("min_stock_level", 0))
        ratio = low_stock / float(total)

        return {
            "total_materials": total,
            "low_stock_count": low_stock,
            "stockout_ratio": ratio,
            "material_risk_score": min(ratio * 80.0, 100.0),
            "status": "STOCKOUT_ALERT" if low_stock > 0 else "SUFFICIENT"
        }
