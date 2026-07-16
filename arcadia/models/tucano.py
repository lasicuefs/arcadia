from typing import ClassVar, Literal

import attrs

from arcadia.models.api.decoder import GeneratesText


@attrs.frozen
class Tucano(GeneratesText):
    owner: ClassVar[str] = "TucanoBR"
    _model: ClassVar[str] = "Tucano-{size}-Instruct"
    size: Literal["1.1B", "2.4B"] = "2.4B"

    @property
    def model(self) -> str:
        size = self.size.replace("B", "")
        return self._model.format(size=size.replace(".", "b") if "." in size else f"{size}b")
