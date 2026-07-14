import pytest
from candor.analysis.reporting import render_analysis
from candor.analysis.pipeline import AnalysisResult
from tests.utils import normalize_output

@pytest.fixture
def golden_analysis():
    return AnalysisResult(
        summary={
            "target": "tesla.com",
            "host": "2.18.51.207",
            "elapsed": "8.72 s",
            "open_ports": ["80/tcp open http", "443/tcp open https"]
        },
        findings=[
            "Host is reachable",
            "HTTP service detected",
            "HTTPS service detected",
            "Reverse DNS indicates Akamai CDN",
            "98 TCP ports filtered"
        ],
        assessment=[
            "Exposure appears consistent with a public-facing website.",
            "No unexpected network services were detected."
        ],
        risk="Informational",
        recommendations=[
            "scan-service tesla.com",
            "whois tesla.com",
            "dig tesla.com",
            "nikto tesla.com (if authorized)"
        ],
        confidence=96
    )

def test_render_analysis_matches_golden_master(golden_analysis, capsys):
    # Render analysis
    render_analysis(golden_analysis)
    captured = capsys.readouterr().out

    # Normalize output
    captured_norm = normalize_output(captured)

    # Load golden master file
    with open("tests/golden_reporting.txt", "r") as f:
        golden_output = normalize_output(f.read())

    # Compare line by line
    captured_lines = [line for line in captured_norm.splitlines() if line.strip()]
    golden_lines = [line for line in golden_output.splitlines() if line.strip()]

    assert len(captured_lines) == len(golden_lines)

    for i, (cap, gold) in enumerate(zip(captured_lines, golden_lines)):
        assert cap == gold, f"Mismatch at line {i+1}: expected '{gold}' but got '{cap}'"
