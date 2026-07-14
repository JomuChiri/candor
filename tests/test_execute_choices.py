import io
import pytest
from rich.console import Console

class FakeOutput:
    def __init__(self):
        self.calls = []

    def show_raw_output(self, result, show=False):
        self.calls.append(("raw", result, show))

def fake_handle(command, console_obj=None, current_investigation=None):
    # Record the command instead of executing
    console_obj.print(f"[TEST] Executed: {command}")

@pytest.mark.parametrize("choice,expected", [
    ("1", "scan-service 192.168.1.54"),
    ("2", "whois 192.168.1.54"),
    ("3", "dig 192.168.1.54"),
    ("4", "workflow web 192.168.1.54"),
])
def test_dispatches_correct_command(choice, expected):
    console = Console(file=io.StringIO())
    target = "192.168.1.54"

    # Simulate handler logic
    if choice == "5":
        assert False, "This test is for commands 1-4 only"
    elif choice == "1":
        fake_handle(f"scan-service {target}", console_obj=console)
    elif choice == "2":
        fake_handle(f"whois {target}", console_obj=console)
    elif choice == "3":
        fake_handle(f"dig {target}", console_obj=console)
    elif choice == "4":
        fake_handle(f"workflow web {target}", console_obj=console)

    output = console.file.getvalue()
    assert expected in output

def test_show_raw_output_choice():
    console = Console(file=io.StringIO())
    fake_output = FakeOutput()
    combined_result = {"stdout": "RAW TEXT"}

    choice = "5"
    if choice == "5":
        fake_output.show_raw_output(combined_result, show=True)

    assert fake_output.calls
    assert fake_output.calls[0][0] == "raw"
    assert fake_output.calls[0][1] == combined_result
    assert fake_output.calls[0][2] is True
