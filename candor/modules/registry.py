from candor.modules.whois.module import WhoisModule
from candor.modules.nmap.module import NmapModule

MODULES = {
    "whois": WhoisModule(),
    "nmap": NmapModule(),
    # add more as you go
}

def get(name):
    return MODULES.get(name)
