<p align="right">
<a href="README.pt-BR.md">Leia em português</a>
</p>

<div align="center">

# ✦ Arcadia ✦

**A research API for language model experimentation at LASIC**

`LLMs` · `Poetry Generation` · `Prompt Evaluation` · `Research Playground`
</div>

<p align="center">
———————————————— 🙡 ————————————————
</p>

## Overview

**Arcadia** is a minimal wrapper for loading PT-BR friendly language models without repeatedly typing model names, package versions, and runtime setup details by hand.

This repository exists to install and run AI models quickly, mainly — but not limited to — in Google Colab, Kaggle or local.

The name points to Arcadia as an imagined landscape of harmony, nature, and reflection. For this research playground, it suggests a space for language, experimentation, and creative exploration with LLMs.


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

For an interactive chat, use `exit`, or `quit` to finish.


## Output Artifacts

Use a directory outside this repository for prompts, templates, responses, poems, evaluations, and other generated documents.

Example in Colab:

```python
from pathlib import Path

OUTPUT_DIR = Path("/content/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

Do not version these artifacts in this repository:

- prompts and prompt templates;
- generated poems;
- raw model responses;
- evaluations produced by judge models;
- documents derived from model outputs.

Notice that the `s*` releases use data-based versioning. They are retained solely for historical purposes and are now deprecated.


## API

See [docs/API.md](docs/API.md) for the public model API, lifecycle rules, output objects, and chat history behavior.

To add another model wrapper, follow [docs/ADDING_MODELS.md](docs/ADDING_MODELS.md).

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

<div align="center">

**Arcadia**<br>
*A poetic gateway for exploring language models within LASIC.*

</div>

<p align="center">🙡 ✦ 🙡</p>
