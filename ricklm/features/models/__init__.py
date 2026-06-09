from typing import Any, Literal, ClassVar

import attrs

from ricklm.shared.models.capabilities import GeneratesText, TextOutput, normalize


__all__ = ["AmadeusVerbo", "Gaia", "Tucano", "TeenyTinyLlama"]


@attrs.frozen
class AmadeusVerbo(GeneratesText):
    owner: ClassVar[str] = "amadeusai"
    _model: ClassVar[str] = "Amadeus-Verbo-FI-Qwen2.5-{size}-PT-BR-Instruct"
    size: Literal["0.5B", "1.5B", "3B", "7B", "14B", "32B", "72B"] = "7B"

    @property
    def model(self) -> str:
        return self._model.format(size=self.size)


@attrs.frozen
class Gaia(GeneratesText):
    owner: ClassVar[str] = "CEIA-UFG"
    _model: ClassVar[str] = "Gemma-3-Gaia-PT-BR-{size}-it"
    size: Literal["4B"] = "4B"

    @property
    def model(self) -> str:
        # 4B => 4b
        size = self.size.replace("B", "b")
        return self._model.format(size=size)


@attrs.frozen
class Tucano(GeneratesText):
    owner: ClassVar[str] = "TucanoBR"
    _model: ClassVar[str] = "Tucano-{size}-Instruct"
    size: Literal["1.1B", "2.4B"] = "2.4B"

    def _normalize_size(self, size: str) -> str:
        assert size.endswith("B"), "Size must end with 'B'"
        if "." in size:
            # "1.3B" => "1b3"
            return size.replace("B", "").replace(".", "b")
        else:
            # "2B" => "2b"
            return size.replace("B", "b")

    @property
    def model(self) -> str:
        size = self._normalize_size(self.size)
        return self._model.format(size=size)


@attrs.frozen
class TeenyTinyLlama(GeneratesText):
    owner: ClassVar[str] = "nicholasKluge"
    _model: ClassVar[str] = "TeenyTinyLlama-{size}-Chat"
    size: Literal["460m"] = "460m"

    @property
    def model(self) -> str:
        return self._model.format(size=self.size)
    
    def ask(
        self,
        prompt: str,
        *,
        remember: bool = False,
        max_new_tokens: int = 512,
        do_sample: bool = True,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> TextOutput:
        if self._pipe is None:
            raise RuntimeError("Pipeline not initialized. Use 'with' statement to initialize the model.")

        instruction = f"<instruction>{prompt}</instruction>"
        response = self._pipe(
            instruction,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature,
            **kwargs,
        )
        output = normalize(response[0]["generated_text"].replace(instruction, "", 1)) # type: ignore
        return TextOutput(output)
