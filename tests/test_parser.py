from candor.parser.intent import parse_intent

def test_scan_defaults():
    intent = parse_intent("scan google.com")
    assert intent.action == "port_scan"

def test_scan_fast():
    intent = parse_intent("scan-fast google.com")
    assert intent.action == "scan-fast"

def test_scan_os():
    intent = parse_intent("scan-os google.com")
    assert intent.action == "scan-os"

def test_whois_lookup():
    intent = parse_intent("whois example.com")
    assert intent.action == "lookup"
