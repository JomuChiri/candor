from candor.modules.base import BaseModule
from .summary import summarize_nmap


class NmapModule(BaseModule):
    name = "nmap"
    category = "Scanning"
    description = "Network discovery and port scanning"
    aliases = ["nmap"]
    default_action = "scan"
    actions = {
        "scan": "Basic port scan",
        "scan-service": "Service/version detection",
        "scan-os": "OS detection",
        "scan-all": "Aggressive full scan",
    }

    summarizer = summarize_nmap

    def build(self, intent):
        target = intent.target
        commands = {

            "scan": [
                "nmap",
                target,
            ],

            "scan-service": [
                "nmap",
                "-sV",
                target,
            ],

            "scan-os": [
                "nmap",
                "-O",
                target,
            ],

            "scan-all": [
                "nmap",
                "-A",
                target,
            ],

        }

        return commands[intent.action]