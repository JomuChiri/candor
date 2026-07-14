# candor/analysis/confidence.py
import random

def score_confidence(summary: dict, findings: list, assessment: list) -> int:
    """
    Stub confidence scoring function.
    Returns a confidence percentage (0–100).
    Currently uses simple heuristics + randomness.
    Later you can replace with ML or rule-based scoring.
    """

    base = 50

    # Heuristic: more findings → higher confidence
    if findings:
        base += min(len(findings) * 5, 20)

    # Heuristic: if summary has host + open_ports → higher confidence
    if summary and summary.get("host") and summary.get("open_ports"):
        base += 20

    # Heuristic: if assessment lines exist → higher confidence
    if assessment:
        base += 10

    # Clamp between 0–100
    confidence = max(0, min(100, base))

    # Add a small random jitter so it doesn’t look static
    confidence += random.randint(-3, 3)
    confidence = max(0, min(100, confidence))

    return confidence
