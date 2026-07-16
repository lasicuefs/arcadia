from typing import Any, ClassVar, Literal

import attrs

from arcadia.models.api.decoder import GeneratesText, TextOutput, normalize


def strip_instruction_echo(text: str, instruction: str) -> str:
    output = normalize(text)

    if instruction in output:
        output = output.replace(instruction, "", 1)

    if "</instruction>" in output:
        output = output.split("</instruction>", 1)[1]

    return normalize(output)


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
        return TextOutput(strip_instruction_echo(response[0]["generated_text"], instruction))
