# candor/modules/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
import subprocess

@dataclass
class ExecutionResult:
    command: list[str]
    stdout: str
    stderr: str
    returncode: int

    @property
    def success(self) -> bool:
        return self.returncode == 0


class BaseModule(ABC):
    """
    Base class for every Candor module.
    """

    name = ""
    category = "General"
    description = ""
    aliases = []
    actions = {}
    supported_targets = []

    summarizer = None

    @abstractmethod
    def build(self, intent):
        """Return the command to execute."""
        pass

    def execute(self, command):
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )
        return ExecutionResult(
            command=command,
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
        )

    def analyze(self, result: ExecutionResult):
        if self.summarizer is None:
            from candor.analysis.analyzer import AnalysisResult
            return AnalysisResult(
                summary="No summarizer available.",
                findings=[],
                recommendations=[],
                risk="INFORMATIONAL",
            )
        # Summarizer must return an AnalysisResult
        return type(self).summarizer(result.stdout)

    @classmethod
    def metadata(cls):
        return {
            "name": cls.name,
            "category": cls.category,
            "description": cls.description,
            "aliases": cls.aliases,
            "actions": list(cls.actions.keys()),
            "supported_targets": cls.supported_targets,
        }

    @classmethod
    def help(cls):
        meta = cls.metadata()
        lines = [
            f"[bold cyan]{meta['name']}[/]",
            "",
            meta["description"],
            "",
            f"Category : {meta['category']}",
            f"Aliases  : {', '.join(meta['aliases'])}",
            "",
            "Actions:",
        ]
        for action, desc in cls.actions.items():
            lines.append(f"  {action:<12} {desc}")
        if cls.supported_targets:
            lines.append("")
            lines.append("Targets : " + ", ".join(cls.supported_targets))
        return "\n".join(lines)
