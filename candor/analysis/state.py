# candor/analysis/state.py

from dataclasses import dataclass, field
from typing import List, Dict
from candor.analysis.analyzer import Recommendation

@dataclass
class InvestigationState:
    host: str
    findings: List[str] = field(default_factory=list)
    surfaces: List[str] = field(default_factory=list)
    executed: List[str] = field(default_factory=list)   # commands already run
    pending: List[Recommendation] = field(default_factory=list)

    def add_findings(self, new_findings: List[str]):
        self.findings.extend(f for f in new_findings if f not in self.findings)

    def add_surfaces(self, new_surfaces: List[str]):
        self.surfaces.extend(s for s in new_surfaces if s not in self.surfaces)

    def add_recommendations(self, recs: List[Recommendation]):
        for r in recs:
            cmd = f"{r.tool} {r.action}"
            if cmd not in [p.tool + " " + p.action for p in self.pending]:
                self.pending.append(r)

    def mark_executed(self, rec: Recommendation):
        cmd = f"{rec.tool} {rec.action}"
        self.executed.append(cmd)
        self.pending = [p for p in self.pending if f"{p.tool} {p.action}" != cmd]

    def next_step(self) -> Recommendation | None:
        """Return the next unexecuted recommendation."""
        if not self.pending:
            return None
        return self.pending[0]
