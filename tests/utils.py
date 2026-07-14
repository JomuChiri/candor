
import re

def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape sequences (color codes, styling) from Rich output.
    """
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]| \[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)

def normalize_output(text: str) -> str:
    """
    Normalize Rich output for Golden Master comparison:
    - Strip ANSI codes
    - Collapse multiple spaces
    - Strip trailing whitespace
    """
    text = strip_ansi(text)
    text = re.sub(r"[ \t]+", " ", text)  # collapse spaces/tabs
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines)
