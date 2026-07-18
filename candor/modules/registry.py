# candor/modules/registry.py

from candor.modules.gobuster import GobusterModule
from candor.modules.nmap import NmapModule
from candor.modules.nikto import NiktoModule
from candor.modules.ffuf import FfufModule
from candor.modules.enum4linux import Enum4linuxModule
from candor.modules.smbclient import SmbclientModule
from candor.modules.rpcclient import RpcclientModule
from candor.modules.netexec import NetExecModule
from candor.modules.bloodhound import BloodhoundModule
from candor.modules.impacket import ImpacketModule
from candor.modules.whois import WhoisModule
from candor.modules.dnsrecon import DnsreconModule
from candor.modules.searchsploit import SearchsploitModule
from candor.modules.dig import DigModule
from candor.modules.nuclei import NucleiModule


class ModuleRegistry:
    def __init__(self):
        self.modules = {
            "gobuster": GobusterModule,
            "nmap": NmapModule,
            "nikto": NiktoModule,
            "ffuf": FfufModule,
            "enum4linux": Enum4linuxModule,
            "smbclient": SmbclientModule,
            "rpcclient": RpcclientModule,
            "netexec": NetExecModule,
            "bloodhound": BloodhoundModule,
            "impacket": ImpacketModule,
            "whois": WhoisModule,
            "dig": DigModule,
            "searchsploit": SearchsploitModule,
            "dnsrecon": DnsreconModule,
            "nuclei": NucleiModule,
        }

    def get(self, name):
        return self.modules.get(name)

    def create(self, name):
        module = self.get(name)
        if module is None:
            raise KeyError(f"Unknown module: {name}")
        return module()

    def list(self):
        return [
            module.metadata()
            for module in self.modules.values()
        ]

    def register(self, name: str, module_class):
        self.modules[name] = module_class

    def resolve(self, token: str):
        """
        Resolve a tool token (canonical name or alias) to a module instance.
        """
        token = token.lower()
        for name, module_class in self.modules.items():
            if token == name or token in getattr(module_class, "aliases", []):
                return module_class()
        raise KeyError(f"Unknown tool '{token}'")

    def by_category(self):
        categories = {}
        for module in self.modules.values():
            meta = module.metadata()
            categories.setdefault(
                meta["category"],
                []
            ).append(meta)
        return categories

    def names(self):
        return sorted(self.modules.keys())

registry = ModuleRegistry()