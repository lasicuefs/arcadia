# Adding New Models

Use this checklist when adding a new Hugging Face model wrapper to Arcadia.

## 1. Choose The Capability Base

Text-generation chat models should inherit from `GeneratesText` in `arcadia.shared.models.capabilities`.

```python
from arcadia.shared.models.capabilities import GeneratesText
```

Add a different capability base only when the model needs a different pipeline task or return shape.

## 2. Add The Model Class

Add the class to `arcadia/features/models/__init__.py`.

### Minimal way

This is encouraged if your model doesn't support variations, like size, quantitization, etc.


```python
from typing import ClassVar, Literal

import attrs


@attrs.frozen
class NewModel(GeneratesText):
    owner: ClassVar[str] = "huggingface-owner"
    model: ClassVar[str] = "Model-Name"
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

Observation: Since you're using `attrs`, `_model` is shown as `model` for class instantiation, but the `model` property will be actually `model`. Also notice that `fronzen` plays a good role here, since you can't change those values once instanciated.

This is equilavent to write:

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

Add the class name to `__all__` in `arcadia/features/models/__init__.py`.

Then re-export it from `arcadia/models.py`:

```python
from arcadia.features.models import NewModel

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
- `rodar.ipynb`

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
