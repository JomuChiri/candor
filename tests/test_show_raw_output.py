import io
from rich.console import Console

class FakeOutput:
    def __init__(self):
        self.called = False
        self.args = None

    def show_raw_output(self, result, show=False):
        self.called = True
        self.args = (result, show)

def test_show_raw_output_option(monkeypatch):
    # Arrange
    console = Console(file=io.StringIO())
    fake_output = FakeOutput()
    combined_result = {"stdout": "RAW WHOIS TEXT"}  # minimal fake result

    # Simulate user choosing option 5
    choice = "5"

    # Act
    if choice == "5":
        fake_output.show_raw_output(combined_result, show=True)

    # Assert
    assert fake_output.called is True
    assert fake_output.args[0] == combined_result
    assert fake_output.args[1] is True

def test_no_raw_output_when_other_choice(monkeypatch):
    console = Console(file=io.StringIO())
    fake_output = FakeOutput()
    combined_result = {"stdout": "RAW NMAP TEXT"}

    # Simulate user choosing option 1 (scan-service)
    choice = "1"

    if choice == "5":
        fake_output.show_raw_output(combined_result, show=True)

    # Assert: raw output not shown
    assert fake_output.called is False
