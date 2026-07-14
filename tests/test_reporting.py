import pytest
from rich.console import Console
from rich.text import Text
from candor.analysis.reporting import render_analysis
from candor.analysis.pipeline import AnalysisResult

@pytest.fixture
def dummy_analysis():
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

def test_render_analysis_outputs_sections(dummy_analysis, capsys):
    # Capture Rich console output
    render_analysis(dummy_analysis)
    captured = capsys.readouterr()

    # Assert key headings are present
    assert "Summary" in captured.out
    assert "Findings" in captured.out
    assert "Assessment" in captured.out
    assert "Recommended Next Steps" in captured.out

    # Assert risk and confidence are displayed
    assert "Overall Risk : INFORMATIONAL" in captured.out
    assert "Confidence   : 96%" in captured.out

    # Assert findings are listed
    assert "HTTP service detected" in captured.out
    assert "Reverse DNS indicates Akamai CDN" in captured.out

    # Assert recommendations are listed
    assert "scan-service tesla.com" in captured.out
    assert "nikto tesla.com" in captured.out
