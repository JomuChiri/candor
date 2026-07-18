import pytest
from candor.analysis.analyzer import AnalysisResult, Finding
from candor.modules.base import BaseModule

class DummyModule(BaseModule):
    # Summarizer returns a list of Finding objects
    @staticmethod
    def summarizer(output: str):
        return [
            Finding(
                signature="22/tcp:ssh",
                service="ssh",
                severity="medium",
                description="OpenSSH detected",
                cve=None,
                recommendations=[]
            )
        ]

def test_analyze_returns_analysisresult():
    dummy = DummyModule()
    # Simulate a result object with stdout
    class Result:
        stdout = "22/tcp open ssh"

    analysis = dummy.analyze(Result())

    # Assertions
    assert isinstance(analysis, AnalysisResult)
    assert isinstance(analysis.findings, list)
    assert all(isinstance(f, Finding) for f in analysis.findings)
    assert len(analysis.findings) == 1
    assert analysis.findings[0].service == "ssh"
