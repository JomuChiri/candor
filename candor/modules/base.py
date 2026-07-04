# candor/modules/base.py
from abc import ABC, abstractmethod

class BaseModule(ABC):
    name: str = ""
    aliases: list[str] = []
    description: str = ""
    actions: dict[str, str] = {}
    supported_targets: list[str] = []

    @abstractmethod
    def build(self, intent):
        pass

    @abstractmethod
    def execute(self, plan):
        pass

    def metadata(self) -> dict:
        """Return structured metadata for this module."""
        return {
            "name": self.name,
            "description": self.description,
            "aliases": self.aliases,
            "actions": list(self.actions.keys()),
            "supported_targets": self.supported_targets,
        }

    def help(self) -> str:
        """Return human‑readable help text."""
        meta = self.metadata()
        lines = [f"[bold cyan]{meta['name']}[/] — {meta['description']}"]
        lines.append(f"Aliases: {', '.join(meta['aliases'])}")
        lines.append("Actions:")
        for action in meta["actions"]:
            lines.append(f"  • {action}")
        if meta["supported_targets"]:
            lines.append(f"Supported targets: {', '.join(meta['supported_targets'])}")
        return "\n".join(lines)
