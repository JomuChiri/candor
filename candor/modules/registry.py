import traceback
import importlib
import pkgutil
import candor.modules
from candor.modules.base import BaseModule

MODULES = {}

def discover_modules():
    package = candor.modules
    for _, name, ispkg in pkgutil.iter_modules(package.__path__):
        # Skip non-tool packages
        if name in ("base", "registry"):
            continue
        try:
            module = importlib.import_module(f"candor.modules.{name}.module")
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, BaseModule) and obj is not BaseModule:
                    instance = obj()
                    MODULES[instance.name] = instance
        except Exception :
            print(f"\nFailed to load {name}")

discover_modules()

def get(name: str):
    return MODULES.get(name)
