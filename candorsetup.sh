#!/bin/bash
# Candor SOC bootstrap script
# Creates full repo structure with base files

# Exit on error
set -e

# Create base files
touch README.md LICENSE CONTRIBUTING.md CHANGELOG.md \
      pyproject.toml requirements.txt .gitignore

# Create docs folder
mkdir -p docs/examples
touch docs/architecture.md docs/roadmap.md docs/cli.md docs/modules.md

# Create main candor package structure
mkdir -p candor/{ai,parser,shell,memory,report,modules,utils}
touch candor/__init__.py candor/cli.py candor/config.py candor/logger.py

# AI providers
touch candor/ai/{provider.py,ollama.py,openai.py,gemini.py,claude.py}

# Parser
touch candor/parser/{intent.py,planner.py,validator.py}

# Shell
touch candor/shell/{execute.py,sandbox.py}

# Memory
touch candor/memory/{history.py,sessions.py,vector.py}

# Report
touch candor/report/{markdown.py,html.py,pdf.py}

# Modules (security tools)
mkdir -p candor/modules/{nmap,dig,whois,dnsrecon,ffuf,gobuster,nuclei,nikto,sqlmap,burp,metasploit,crackmapexec,bloodhound,responder,impacket}
mkdir -p candor/modules/{wazuh,suricata,zeek,osquery,elastic,sigma,yara}
mkdir -p candor/modules/{windows,linux,docker,vmware}

# Tests
mkdir -p tests

echo "Candor SOC repo structure created successfully!"
