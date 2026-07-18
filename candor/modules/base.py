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


@dataclass
class AnalysisResult:
    summary: str
    findings: dict
    recommendations: list[str]
    risk: str = "Unknown"


class BaseModule(ABC):
    """
    Base class for every Candor module.

    Every module only needs to implement:

        build(intent)

    Everything else has sensible defaults.
    """

    name = ""
    category = "General"
    description = ""
    aliases = []
    actions = {}
    supported_targets = []

    summarizer = None

    #
    # ---------- Required ----------
    #

    @abstractmethod
    def build(self, intent):
        """
        Return the command to execute.

        Example:

        ["nmap", "-sV", target]
        """
        pass

    #
    # ---------- Default execution ----------
    #

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

    #
    # ---------- Analysis ----------
    #

    def analyze(self, result: ExecutionResult):

        if self.summarizer is None:

            return AnalysisResult(
                summary="No summarizer available.",
                findings={},
                recommendations=[],
            )

        findings = self.summarizer(result.stdout)

        return AnalysisResult(
            summary="Analysis complete.",
            findings=findings,
            recommendations=[],
        )

    #
    # ---------- Metadata ----------
    #

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
            lines.append(
                "Targets : " +
                ", ".join(cls.supported_targets)
            )

        return "\n".join(lines)