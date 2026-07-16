<p align="right">
<a href="README.md">Read in English</a>
</p>

<div align="center">

# ✦ Arcadia ✦

**Uma API de pesquisa para experimentação com modelos de linguagem no LASIC**

`LLMs` · `Geração de Poesia` · `Avaliação de Prompts` · `Research Playground`
</div>

<p align="center">
———————————————— 🙡 ————————————————
</p>

## Visão Geral

**Arcadia** é um wrapper mínimo para carregar modelos de linguagem amigáveis a PT-BR sem precisar digitar repetidamente nomes de modelos, versões de pacotes e detalhes de configuração do runtime.

O nome aponta para Arcadia como uma paisagem imaginada de harmonia, natureza e reflexão. Para este ambiente de pesquisa, ele sugere um espaço de linguagem, experimentação e exploração criativa com LLMs.

Este repositório existe para instalar e executar modelos de IA rapidamente, principalmente — mas não limitado a — Google Colab, Kaggle ou localmente.


## Como Usar

Abra [`executar.ipynb`](https://colab.research.google.com/github/RickBarretto/llm-playground/blob/main/executar.ipynb) no Colab e habilite um runtime com GPU em `Runtime` -> `Change runtime type` -> `T4 GPU` ou melhor.

Para testar uma branch ou tag específica:

```python
GIT_REF = "main"  # branch ou tag

!rm -rf /content/llm-playground
!git clone https://github.com/RickBarretto/llm-playground /content/llm-playground
%cd /content/llm-playground
!git fetch --all --tags
!git checkout $GIT_REF
!pip install -U /content/llm-playground
```


## Execução Mínima

```python
from pathlib import Path
from arcadia import models

OUTPUT_DIR = Path("/content/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

model = models.AmadeusVerbo("3B")

with model as m:
    output = m.ask("Escreva uma frase curta sobre o Brasil.")
    print(output)
    (OUTPUT_DIR / "ask.txt").write_text(output, encoding="utf-8")
```


## Chat

```python
from arcadia import models

model = models.AmadeusVerbo("3B")

with model as m:
    history = m.chat([
        "Escreva uma frase sobre o Brasil.",
        "Agora transforme essa frase em um verso.",
    ])

    print(history[-1])
    print(history[-1].ai)
    print(history.last.ai)
```

Para um chat interativo, use `sair` para finalizar.


## Artefatos De Saída

Use um diretório fora deste repositório para prompts, modelos de prompt, respostas, poemas, avaliações e outros documentos gerados.

Exemplo no Colab:

```python
from pathlib import Path

OUTPUT_DIR = Path("/content/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

Não versione estes artefatos neste repositório:

- prompts e modelos de prompt;
- poemas gerados;
- respostas brutas de modelos;
- avaliações produzidas por modelos juízes;
- documentos derivados de saídas de modelos.

Observe que as releases `s*` utilizam versionamento baseado em dados. Elas são mantidas apenas para preservar o histórico, mas estão descontinuadas.


## API

Consulte [docs/API.md](docs/API.md) para a API pública dos modelos, as regras de ciclo de vida, os objetos de saída e o comportamento do histórico de chat.

Para adicionar outro wrapper de modelo, siga [docs/ADDING_MODELS.md](docs/ADDING_MODELS.md).

`ask()` retorna a resposta do modelo como texto UTF-8 normalizado:

```python
with model as m:
    output = m.ask("Meu prompt")
    print(output)
```

`chat()` retorna um histórico indexável. `history[-1]` renderiza a última rodada usuário/modelo, enquanto `history[-1].ai` ou `history.last.ai` retorna apenas a resposta do modelo:

```python
with model as m:
    history = m.chat(["Meu prompt"])
    print(history[-1])
    print(history[-1].ai)
    print(history.last.ai)
```

<div align="center">

**Arcadia**<br>
*Um portal poético para explorar modelos de linguagem dentro do LASIC.*

</div>

<p align="center">🙡 ✦ 🙡</p>
