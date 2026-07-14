import pytest
from candor.analysis.pipeline import analyze, AnalysisResult

class DummyIntent:
    def __init__(self, tool, action="scan", target="example.com"):
        self.tool = tool
        self.action = action
        self.target = target

class DummyResult:
    def __init__(self, stdout="", stderr="", status="success"):
        self.stdout = stdout
        self.stderr = stderr
        self.status = status

def test_whois_analysis_returns_summary(dummy_whois_output):
    intent = DummyIntent(tool="whois", action="lookup", target="tesla.com")
    result = DummyResult(stdout=dummy_whois_output)

    analysis = analyze(intent, result)

    assert isinstance(analysis, AnalysisResult)
    assert "Domain Name" in analysis.summary.get("raw", result.stdout)
    assert analysis.findings == []
    assert analysis.recommendations == []
    assert analysis.risk in ["Informational", "LOW"]

def test_nmap_analysis_returns_expected_fields(dummy_nmap_output):
    intent = DummyIntent(tool="nmap", action="scan-fast", target="tesla.com")
    result = DummyResult(stdout=dummy_nmap_output)

    analysis = analyze(intent, result)

    assert isinstance(analysis, AnalysisResult)
    assert "host" in analysis.summary
    assert "open_ports" in analysis.summary
    assert any("80/tcp" in p for p in analysis.summary["open_ports"])
    assert len(analysis.findings) > 0
    assert analysis.assessment is not None
    assert all(isinstance(r, str) for r in analysis.recommendations)
    assert analysis.risk in ["Informational", "Medium", "High"]
    assert isinstance(analysis.confidence, int)
    assert 0 <= analysis.confidence <= 100
