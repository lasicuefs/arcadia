from collections.abc import Iterable, Iterator
from typing import Any
import unicodedata

import attrs
from transformers import Pipeline

from ricklm.shared.models.base import Model


def normalize(response: str) -> str:
    text = response.strip().replace("\\n", "\n").replace("\\t", "\t")
    return unicodedata.normalize("NFC", text)


def generated_content(response: Any) -> str:
    generated = response[0]["generated_text"]

    if isinstance(generated, list):
        message = generated[-1]
        if isinstance(message, dict):
            return str(message["content"])
        return str(message)

    return str(generated)


class TextOutput(str):
    ai: str

    def __new__(cls, ai: str) -> "TextOutput":
        output = normalize(ai)
        instance = super().__new__(cls, output)
        instance.ai = output
        return instance

    def __repr__(self) -> str:
        return str(self)


class ChatTurn(str):
    user: str
    ai: str
    model: str

    def __new__(cls, *, user: str, ai: str, model: str) -> "ChatTurn":
        user = normalize(user)
        ai = normalize(ai)
        output = "\n\n".join(
            [
                "Usuário:",
                user,
                f"{model}:",
                ai,
            ]
        )
        instance = super().__new__(cls, output)
        instance.user = user
        instance.ai = ai
        instance.model = model
        return instance

    def __repr__(self) -> str:
        return str(self)
    
    @property
    def llm(self) -> str:
        return self.ai
    
    @property
    def assistant(self) -> str:
        return self.ai
    
    @property
    def system(self) -> str:
        return self.ai

    @property
    def human(self) -> str:
        return self.user
    
    @property
    def me(self) -> str:
        return self.user


@attrs.define
class ChatHistory:
    model: "GeneratesText"
    prompts: Iterable[str] | None = None
    exit_words: tuple[str, ...] = ("exit", "quit", "sair")
    history: list[ChatTurn] = attrs.field(factory=list, init=False)
    _consumed: bool = attrs.field(default=False, init=False)

    def __iter__(self) -> Iterator[ChatTurn]:
        if self._consumed:
            yield from self.history
            return

        prompts = self.prompts if self.prompts is not None else self._prompt_loop()

        for prompt in prompts:
            output = self.model.ask(prompt, remember=True)
            turn = ChatTurn(user=normalize(prompt), ai=output.ai, model=str(self.model))
            self.history.append(turn)
            yield turn

        self._consumed = True

    def __getitem__(self, index: int) -> ChatTurn:
        self._consume()
        return self.history[index]

    def __len__(self) -> int:
        self._consume()
        return len(self.history)

    def _consume(self) -> None:
        if not self._consumed:
            for _ in self:
                pass

    @property
    def last(self) -> ChatTurn:
        return self[-1]

    def __str__(self) -> str:
        self._consume()
        return "\n\n---\n\n".join(str(turn) for turn in self.history)

    def __repr__(self) -> str:
        return str(self)

    def _prompt_loop(self) -> Iterator[str]:
        while True:
            prompt = input("> ").strip()
            if prompt.lower() in self.exit_words:
                break
            if prompt:
                yield prompt


@attrs.frozen
class GeneratesText(Model):
    _pipe: Pipeline | None = attrs.field(default=None, init=False, repr=False, eq=False, hash=False)
    _messages: list[dict[str, str]] = attrs.field(
        factory=list,
        init=False,
        repr=False,
        eq=False,
        hash=False,
    )

    def __enter__(self):
        object.__setattr__(self, "_pipe", self.pipeline("text-generation"))
        self.reset()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pipeline.cache_clear()
        self.reset()
        object.__setattr__(self, "_pipe", None)

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

        prompt = normalize(prompt)
        messages = [*self._messages, {"role": "user", "content": prompt}]
        response = self._pipe(
            messages,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature,
            **kwargs,
        )
        output = TextOutput(generated_content(response))

        if remember:
            object.__setattr__(
                self,
                "_messages",
                [*messages, {"role": "assistant", "content": output.ai}],
            )

        return output

    def chat(self, prompts: Iterable[str] | None = None) -> ChatHistory:
        return ChatHistory(self, prompts)

    def reset(self) -> None:
        object.__setattr__(self, "_messages", [])

    def text(self, prompt: str) -> str:
        return str(self.ask(prompt))
