import pytest

@pytest.fixture
def dummy_whois_output():
    return """Domain Name: TESLA.COM
Registrar: MARKMONITOR INC.
Creation Date: 1992-11-23
Updated Date: 2025-10-01
Expiration Date: 2030-11-22
Name Server: NS1.MARKMONITOR.COM
Name Server: NS2.MARKMONITOR.COM
"""

@pytest.fixture
def dummy_nmap_output():
    return """Starting Nmap 7.99 ( https://nmap.org ) at 2026-07-09 05:42 -0500
Nmap scan report for tesla.com (2.18.51.207)
Host is up (0.28s latency).
Other addresses for tesla.com (not scanned): 23.7.244.207 2.18.48.207
rDNS record for 2.18.51.207: a2-18-51-207.deploy.static.akamaitechnologies.com
Not shown: 98 filtered tcp ports (no-response)
PORT    STATE SERVICE
80/tcp  open  http
443/tcp open  https
Nmap done: 1 IP address (1 host up) scanned in 8.72 seconds
"""
