# Adding New Models

Use this checklist when adding a new Hugging Face model wrapper to Arcadia.

## 1. Choose The Capability Base

Text-generation chat models should inherit from `GeneratesText` in `arcadia.models.api.decoder`.

```python
from arcadia.models.api.decoder import GeneratesText
```

Add a different capability base only when the model needs a different pipeline task or return shape.

## 2. Add The Model Class

Add the class to a dedicated file under `arcadia/models/`, for example `arcadia/models/new_model.py`.
Keep reusable runtime behavior in `arcadia/models/api/`; model files should only describe Hugging Face ownership, repository-name formatting, and any model-specific prompt or output handling.

### Minimal way

Use this when your model does not support variations like size or quantization.


```python
from typing import ClassVar, Literal

import attrs


@attrs.frozen
class NewModel(GeneratesText):
    owner: ClassVar[str] = "huggingface-owner"
    _model: ClassVar[str] = "Model-Name"
```

### With size variation

```python
from typing import ClassVar, Literal

import attrs


@attrs.frozen
class NewModel(GeneratesText):
    owner: ClassVar[str] = "huggingface-owner"
    _model: ClassVar[str] = "Model-Name-{size}-Instruct"
    size: Literal["1B", "3B"] = "3B"

    @property
    def model(self) -> str:
        return self._model.format(size=self.size)
```

Keep the wrapper small:

- Use `owner` for the Hugging Face organization or user.
- Use `_model` for the Hugging Face repository name template.
- Use `size` as a `Literal` when the model family has fixed supported sizes.
- Override `model` only for name formatting.
- Override `ask()` only when the model requires a special prompt format or output cleanup.

Observation: `attrs.frozen` keeps wrapper instances immutable after they are created.

This is equivalent to write:

```python
class NewModel(GeneratesText):
    owner: ClassVar[str] = "huggingface-owner"
    _model: ClassVar[str] = "Model-Name-{size}-Instruct"

    def __init__(self, size: Literal["1B", "3B"] = "3B") -> None:
        self.size = size

    @property
    def model(self) -> str:
        return self._model.format(size=self.size)
```

## 3. Export The Class

Import the class in `arcadia/models/__init__.py` and add its name to `__all__`:

```python
from arcadia.models.new_model import NewModel

__all__ = [
    "NewModel",
]
```

Preserve the existing exports when adding the new one.

## 4. Document User-Facing Availability

Update the model table in:

- `README.md`
- `README.pt-BR.md`
- `play.ipynb`
- `executar.ipynb`

Include:

- wrapper class name;
- supported sizes;
- default size;
- Hugging Face collection or model URL.

If the model needs different usage instructions, add a short note near the table.

## 5. Verify The Wrapper

At minimum, verify the model id without downloading weights:

```python
from arcadia import models

model = models.NewModel("3B")
print(model.id)
print(model.huggginface)
```

For a runtime check in Colab or another GPU environment:

```python
from arcadia import models

model = models.NewModel("3B")

with model as m:
    print(m.ask("Escreva uma frase curta sobre o Brasil."))
```

For chat behavior:

```python
with model as m:
    history = m.chat([
        "Escreva uma frase sobre o Brasil.",
        "Agora transforme essa frase em um verso.",
    ])
    print(history.last.ai)
```

## 6. Release Runtime Resources

When testing multiple models in the same runtime, release the previous model before loading the next one:

```python
model.release()
del model
```

This clears Python memory, CUDA cache when available, and the local Hugging Face cache for that model.
