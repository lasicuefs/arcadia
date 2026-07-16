from typing import ClassVar, Literal

import attrs

from arcadia.models.api.decoder import GeneratesText


@attrs.frozen
class Gaia(GeneratesText):
    owner: ClassVar[str] = "CEIA-UFG"
    _model: ClassVar[str] = "Gemma-3-Gaia-PT-BR-{size}-it"
    size: Literal["4B"] = "4B"

    @property
    def model(self) -> str:
        return self._model.format(size=self.size.replace("B", "b"))
