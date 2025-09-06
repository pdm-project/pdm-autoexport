from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:
    from pdm.project import Project


@dataclass
class ExportConfig:
    filename: str
    format: str = "requirements"
    groups: Iterable[str] = ("default",)
    without_hashes: bool = False
    pyproject: bool = False

    def __post_init__(self):
        if self.format not in ("requirements",):
            raise ValueError(
                f"Unsupported format: {self.format}, now only requirements is supported"
            )
        if not self.groups:
            raise ValueError("No groups specified")


def export_config(project: Project) -> Iterable[ExportConfig]:
    """
    Load the auto-export config.
    """
    tool_settings = project.pyproject.settings
    return (
        ExportConfig(
            filename=item["filename"],
            format=item.get("format", "requirements"),
            groups=item.get("groups", ["default"]),
            without_hashes=item.get("without-hashes", False),
            pyproject=item.get("pyproject", False),
        )
        for item in tool_settings.get("autoexport", [])
    )


def run_auto_export(project: Project, dry_run: bool, **kwargs: Any) -> None:
    """
    Run the auto-export hook.
    """
    if dry_run:
        return
    core = project.core
    dev_groups = set(project.pyproject.dev_dependencies)
    for config in export_config(project):
        group_args = ["--no-default"]
        if dev_groups.isdisjoint(config.groups):
            group_args.append("--prod")
        for group in config.groups:
            group_args.extend(["--group", group])
        hash_args = ["--without-hashes"] if config.without_hashes else []
        pyproject_args = ["--pyproject"] if config.pyproject else []
        args = [
            "export",
            "--format",
            config.format,
            *group_args,
            *hash_args,
            *pyproject_args,
            "--output",
            os.path.join(project.root, config.filename),
        ]
        core.main(args, obj=project)
