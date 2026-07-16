from typing import ClassVar, Literal

import attrs

from arcadia.models.api.decoder import GeneratesText


@attrs.frozen
class AmadeusVerbo(GeneratesText):
    owner: ClassVar[str] = "amadeusai"
    _model: ClassVar[str] = "Amadeus-Verbo-FI-Qwen2.5-{size}-PT-BR-Instruct"
    size: Literal["0.5B", "1.5B", "3B", "7B", "14B", "32B", "72B"] = "7B"

    @property
    def model(self) -> str:
        return self._model.format(size=self.size)
