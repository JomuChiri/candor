"""
candor/analysis/signatures.py

Knowledge base used by the analysis pipeline.

SERVICE_SIGNATURES
    Generic information about services discovered during reconnaissance.

VULNERABILITY_SIGNATURES
    Known vulnerable software versions or fingerprints.

The analyzer should perform case-insensitive substring matching rather
than exact string equality.
"""

# ---------------------------------------------------------------------
# Generic service intelligence
# ---------------------------------------------------------------------

SERVICE_SIGNATURES = {
    "ftp": {
        "severity": "medium",
        "description": "FTP service detected.",
        "recommendations": [
            {
                "tool": "nmap",
                "action": "script",
                "arguments": {"script": "ftp-anon", "target": "{target}"},
                "reason": "Check for anonymous login",
                "confidence": 0.8,
            }
        ],
    },

    "http": {
        "severity": "medium",
        "description": "HTTP service detected.",
        "recommendations": [
            {
                "tool": "nikto",
                "action": "scan",
                "arguments": {"target": "{target}"},
                "reason": "Identify common web vulnerabilities",
                "confidence": 0.9,
            },
            {
                "tool": "gobuster",
                "action": "dir",
                "arguments": {"target": "{target}"},
                "reason": "Discover hidden directories",
                "confidence": 0.85,
            },
            {
                "tool": "nuclei",
                "action": "scan",
                "arguments": {"target": "{target}"},
                "reason": "Run vulnerability templates",
                "confidence": 0.9,
            },
        ],
    },

    "microsoft-ds": {
        "severity": "high",
        "description": "SMB service detected.",
        "recommendations": [
            {
                "tool": "enum4linux",
                "action": "scan",
                "arguments": {"target": "{target}"},
                "reason": "Enumerate SMB shares and users",
                "confidence": 0.9,
            },
            {
                "tool": "smbclient",
                "action": "list",
                "arguments": {"target": "{target}"},
                "reason": "List available SMB shares",
                "confidence": 0.85,
            },
        ],
    },
}

# ---------------------------------------------------------------------
# Known vulnerable software
# ---------------------------------------------------------------------

VULNERABILITY_SIGNATURES = {
    "vsftpd 2.3.4": {
        "severity": "critical",
        "cve": "CVE-2011-2523",
        "description": "Backdoored FTP server allowing unauthenticated shell access.",
        "recommendations": [
            {
                "tool": "searchsploit",
                "action": "search",
                "arguments": {"query": "vsftpd 2.3.4"},
                "reason": "Look for public exploits",
                "confidence": 0.95,
            },
            {
                "tool": "nmap",
                "action": "script",
                "arguments": {"script": "ftp-vsftpd-backdoor", "target": "{target}"},
                "reason": "Verify backdoor via NSE script",
                "confidence": 0.9,
            },
            {
                "tool": "metasploit",
                "action": "exploit",
                "arguments": {"module": "exploit/unix/ftp/vsftpd_234_backdoor"},
                "reason": "Known backdoor exploit",
                "confidence": 0.98,
            },
        ],
    },

    "apache httpd 2.2": {
        "severity": "medium",
        "status": "EOL",
        "description": "Legacy Apache release.",
        "recommendations": [
            {
                "tool": "nikto",
                "action": "scan",
                "arguments": {"target": "{target}"},
                "reason": "Identify insecure HTTP methods and CVEs",
                "confidence": 0.85,
            },
            {
                "tool": "searchsploit",
                "action": "search",
                "arguments": {"query": "Apache 2.2"},
                "reason": "Check for known exploits",
                "confidence": 0.8,
            },
        ],
    },

    "tomcat": {
        "severity": "high",
        "description": "Apache Tomcat detected.",
        "recommendations": [
            {
                "tool": "nuclei",
                "action": "scan",
                "arguments": {"target": "{target}"},
                "reason": "Check for Tomcat CVEs",
                "confidence": 0.9,
            },
            {
                "tool": "gobuster",
                "action": "dir",
                "arguments": {"target": "{target}"},
                "reason": "Discover Tomcat admin panels",
                "confidence": 0.85,
            },
        ],
    },

    "samba 3.": {
        "severity": "high",
        "description": "Legacy Samba version.",
        "recommendations": [
            {
                "tool": "searchsploit",
                "action": "search",
                "arguments": {"query": "Samba 3"},
                "reason": "Look for public exploits",
                "confidence": 0.9,
            },
            {
                "tool": "enum4linux",
                "action": "scan",
                "arguments": {"target": "{target}"},
                "reason": "Enumerate users and shares",
                "confidence": 0.85,
            },
        ],
    },
}

# ---------------------------------------------------------------------
# Severity ranking
# ---------------------------------------------------------------------

SEVERITY_SCORE = {
    "informational": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}
