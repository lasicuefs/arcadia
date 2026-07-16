# API Reference

Arcadia exposes its user-facing API through `arcadia.models`.

```python
from arcadia import models
```

Supported model wrappers live in separate modules under `arcadia.models` and are re-exported from `arcadia.models` for user code. The `arcadia.models.api` package contains internal base classes and runtime helpers.

## Model Classes

Each model class is an immutable configuration object. Instantiate it with an optional `size`, then use it as a context manager before generating text.

| Class | Default size | Available sizes |
| --- | --- | --- |
| `models.AmadeusVerbo` | `7B` | `0.5B`, `1.5B`, `3B`, `7B`, `14B`, `32B`, `72B` |
| `models.Gaia` | `4B` | `4B` |
| `models.Tucano` | `2.4B` | `1.1B`, `2.4B` |
| `models.TeenyTinyLlama` | `460m` | `460m` |

```python
model = models.AmadeusVerbo("3B")
```

Common properties:

- `model.model`: Hugging Face model name without owner.
- `model.id`: full Hugging Face model id, for example `amadeusai/Amadeus-Verbo-FI-Qwen2.5-3B-PT-BR-Instruct`.
- `model.huggginface`: Hugging Face model URL.

## Lifecycle

Model pipelines are loaded inside a context manager.

```python
with model as m:
    output = m.ask("Escreva uma frase curta sobre o Brasil.")
```

Calling generation methods outside the context manager raises `RuntimeError`, because the Transformers pipeline has not been initialized.

When the context exits, Arcadia clears the cached pipeline reference and resets the in-memory conversation. To explicitly free memory and remove the local Hugging Face cache for a model, call:

```python
model.release()
```

Use `release()` before switching models in constrained environments such as Colab.

## Text Generation

### `ask(prompt, *, remember=False, max_new_tokens=512, do_sample=True, temperature=0.7, **kwargs)`

Generates one model response.

```python
with model as m:
    output = m.ask("Meu prompt")
    print(output)
    print(output.ai)
```

Returns a `TextOutput`, which behaves like `str` and also exposes the normalized response through `.ai`.

Parameters:

- `prompt`: user prompt.
- `remember`: when `True`, stores the user and assistant messages in the current context so the next `ask()` call can continue the conversation.
- `max_new_tokens`, `do_sample`, `temperature`: forwarded to the Transformers pipeline.
- `**kwargs`: additional keyword arguments forwarded to the Transformers pipeline.

### `text(prompt)`

Convenience wrapper around `ask(prompt)` that returns a plain `str`.

```python
with model as m:
    response = m.text("Meu prompt")
```

## Chat

### `chat(prompts=None)`

Creates a `ChatHistory` object.

With a prompt list, iteration runs the prompts in order:

```python
with model as m:
    history = m.chat([
        "Escreva uma frase sobre o Brasil.",
        "Agora transforme essa frase em um verso.",
    ])

    for turn in history:
        print(turn)
```

Without prompts, `chat()` starts an interactive prompt loop. The default exit words are `exit`, `quit`, and `sair`.

Each item is a `ChatTurn`, which behaves like `str` and exposes:

- `.user`, `.human`, `.me`: the normalized user prompt.
- `.ai`, `.llm`, `.assistant`, `.system`: the normalized model response.
- `.model`: model display name for the turn.

`ChatHistory` is indexable after generation:

```python
print(history[-1])
print(history[-1].ai)
print(history.last.ai)
```

## Normalization Helpers

Arcadia normalizes generated text to NFC Unicode and converts escaped `\n` and `\t` sequences into real newline and tab characters before returning output objects.

The helper functions and classes under `arcadia.models.api` are internal implementation details unless a future feature explicitly promotes them to the public API.
