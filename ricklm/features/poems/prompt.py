from __future__ import annotations

from pathlib import Path

import attrs

__all__ = ["Prompt"]


def load_toml(file: Path) -> dict:
    try:
        import tomllib
    except ModuleNotFoundError:
        import toml

        with open(file, "r", encoding="utf-8") as f:
            return toml.load(f)

    with open(file, "rb") as f:
        return tomllib.load(f)


@attrs.frozen(kw_only=True)
class Prompt:
    style: str = attrs.field()
    context: str = attrs.field(default="")
    examples: list[str] = attrs.field(factory=list) # type: ignore

    @classmethod
    def from_toml(cls, file: Path) -> "Prompt":
        """Load a Prompt from a TOML file path.

        Expects a TOML structure like the example in the workspace
        where `general.style` and `general.context` exist and
        `[[poems]]` entries may contain `sample` strings.
        """
        data = load_toml(file)

        general = data.get("general", {})
        style = general.get("style", "")
        context = general.get("context", "")

        examples: list[str] = []
        poems: list[dict[str, str]] = data.get("poems") or []
        
        for entry in poems:
            if (sample := entry.get("sample")):
                examples.append(sample.strip())

        return cls(style=style, context=context.strip(), examples=examples)
