# candor/analysis/model.py
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AnalysisResult:
    """
    Standardized analysis result returned by modules.
    """
    summary: str
    findings: dict[str, Any] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)
