import io
from rich.console import Console

def fake_step(tool_name):
    class Step:
        def __init__(self, tool):
            self.tool = tool
    return Step(tool_name)

def test_capture_message_includes_tool(monkeypatch):
    # Arrange: capture console output
    console = Console(file=io.StringIO())
    step = fake_step("whois")

    # Act: print the capture message
    console.print(f"{step.tool.upper()} output captured. Use 'Show raw output' to view full text.")

    # Assert: check the message
    output = console.file.getvalue()
    assert "WHOIS output captured" in output

def test_capture_message_dynamic_tool(monkeypatch):
    console = Console(file=io.StringIO())
    step = fake_step("nmap")

    console.print(f"{step.tool.upper()} output captured. Use 'Show raw output' to view full text.")

    output = console.file.getvalue()
    assert "NMAP output captured" in output
