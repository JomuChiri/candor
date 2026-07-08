# candor/modules/registry.py
import importlib
import pkgutil
import candor.modules
import os

from candor.modules.base import BaseModule
from candor.modules.nmap import NmapModule
from candor.modules.whois import WhoisModule
# add other modules...

DEBUG = os.getenv("CANDOR_DEBUG", "0") == "1"
MODULES = {
    "nmap": NmapModule,
    "whois": WhoisModule,
    # ...
}

def get(name):
    return MODULES.get(name)

def list_by_category():
    categories = {}
    for module in MODULES.values():
        meta = module.metadata()
        categories.setdefault(meta["category"], []).append(meta)
    return categories

def discover_modules():
    package = candor.modules
    for _, name, ispkg in pkgutil.iter_modules(package.__path__):
        # Skip non‑tool packages
        if name in ("base", "registry"):
            continue
        try:
            module = importlib.import_module(f"candor.modules.{name}.module")
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, BaseModule) and obj is not BaseModule:
                    instance = obj()
                    MODULES[instance.name] = instance
                    if DEBUG:
                        print(f"Loaded module: {instance.name}")
        except Exception as e:
            if DEBUG:
                print(f"Failed to load {name}: {e}")

# Run discovery at import time
discover_modules()

def get(name: str):
    return MODULES.get(name)
