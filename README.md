# Arcadia

> Idealized, unspoiled natural landscape. [^1]

This repository exists to install and run AI models quickly, mainly in Google Colab.

It versions only the execution code, notebook, and documentation for the runtime workflow. Prompts, templates, and model-generated outputs should not be versioned here.

## How To Use

Open [`play.ipynb`](https://colab.research.google.com/github/RickBarretto/llm-playground/blob/main/play.ipynb) in Colab and enable a GPU runtime with `Runtime` -> `Change runtime type` -> `T4 GPU` or better.

To test a specific branch or tag:

```python
GIT_REF = "main"  # branch or tag

!rm -rf /content/llm-playground
!git clone https://github.com/RickBarretto/llm-playground /content/llm-playground
%cd /content/llm-playground
!git fetch --all --tags
!git checkout $GIT_REF
!pip install -U /content/llm-playground
```

## Where To Save Outputs

Use a directory outside this repository for prompts, templates, responses, poems, evaluations, and other generated documents. Ideally, point `OUTPUT_DIR` to a separate repository inside an Obsidian vault.

Example in Colab:

```python
from pathlib import Path

OUTPUT_DIR = Path("/content/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

## Minimal Run

```python
from pathlib import Path
from arcadia import models

OUTPUT_DIR = Path("/content/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

model = models.AmadeusVerbo("3B")

with model as m:
    output = m.ask("Write a short sentence about Brazil.")
    print(output)
    (OUTPUT_DIR / "ask.txt").write_text(output, encoding="utf-8")
```

## Chat

```python
from arcadia import models

model = models.AmadeusVerbo("3B")

with model as m:
    history = m.chat([
        "Write a sentence about Brazil.",
        "Now turn that sentence into a verse.",
    ])

    print(history[-1])
    print(history[-1].ai)
    print(history.last.ai)
```

For an interactive chat, use `sair`, `exit`, or `quit` to finish.

## API Reference

See [docs/API.md](docs/API.md) for the public model API, lifecycle rules, output objects, and chat history behavior.

To add another model wrapper, follow [docs/ADDING_MODELS.md](docs/ADDING_MODELS.md).

## Prompts And Templates

Prompts and templates should live outside this repository, next to the generated outputs they produce.

The preferred layout is a separate repository inside an Obsidian vault. Keep the prompt, generated response, evaluation, and derived documents together there so their history follows the experiment instead of the runtime code.

## LASIC's Arcadia

`arcadia` is a minimal wrapper for loading a few PT-BR friendly models without repeatedly typing model names and package versions by hand.

```python
from arcadia import models

model = models.AmadeusVerbo("3B")
```

`ask()` returns the model response as normalized UTF-8 text:

```python
with model as m:
    output = m.ask("My prompt")
    print(output)
```

`chat()` returns an indexable history. `history[-1]` renders the latest user/model turn, while `history[-1].ai` or `history.last.ai` returns only the model response:

```python
with model as m:
    history = m.chat(["My prompt"])
    print(history[-1])
    print(history[-1].ai)
    print(history.last.ai)
```

## Versioning

This repository versions only the execution environment:

- the `arcadia` package code;
- the execution notebook;
- documentation for the execution workflow.

Do not version these artifacts in this repository:

- prompts and prompt templates;
- generated poems;
- raw model responses;
- evaluations produced by judge models;
- documents derived from model outputs.

These artifacts depend on the prompt, model, and execution settings, not only on the code. They should live in a separate repository, preferably inside an Obsidian vault.


[^1]: https://poemanalysis.com/definition/arcadia/
