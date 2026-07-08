# candor/parser/confidence.py

def assess_confidence(intent, candidates):
    """
    Assess confidence in parser decision.
    If confidence is low, return candidate options.
    """
    if intent.confidence < 0.6:  # threshold
        return {
            "status": "low",
            "candidates": candidates
        }
    return {"status": "high"}
