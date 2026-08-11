from typing import Dict, Any

def normalize_risk_score(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Clamps and normalizes risk scores within a [0.0, 100.0] range."""
    return min(max(float(value), min_val), max_val)

def categorize_risk_level(score: float) -> str:
    """Categorizes numerical risk score into standardized enterprise risk levels."""
    score = normalize_risk_score(score)
    if score >= 70.0:
        return "CRITICAL"
    elif score >= 40.0:
        return "HIGH"
    elif score >= 20.0:
        return "MODERATE"
    else:
        return "LOW"
