# Arcadia

> Paisagem natural idealizada e intocada. [^1]

Este repositório existe para instalar e executar modelos de IA rapidamente, principalmente no Google Colab.

Ele versiona apenas o código de execução, o notebook e a documentação do fluxo de trabalho em tempo de execução. Prompts, modelos de prompt e saídas geradas por modelos não devem ser versionados aqui.

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

## Onde Salvar Saídas

Use um diretório fora deste repositório para prompts, modelos de prompt, respostas, poemas, avaliações e outros documentos gerados. Idealmente, salve suas saídas para um repositório separado dentro de um cofre (Vault) do Obsidian.

Exemplo no Colab:

```python
from pathlib import Path

OUTPUT_DIR = Path("/content/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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

## Referência Da API

Consulte [docs/API.md](docs/API.md) para a API pública dos modelos, as regras de ciclo de vida, os objetos de saída e o comportamento do histórico de chat.

Para adicionar outro wrapper de modelo, siga [docs/ADDING_MODELS.md](docs/ADDING_MODELS.md).

## Prompts E Modelos De Prompt

Prompts e modelos de prompt devem ficar fora deste repositório, junto das saídas geradas por eles.

O layout preferido é um repositório separado dentro de um cofre do Obsidian. Mantenha o prompt, a resposta gerada, a avaliação e os documentos derivados juntos nesse local, para que o histórico acompanhe o experimento em vez do código de execução.

## Arcadia Do LASIC

`arcadia` é um wrapper mínimo para carregar alguns modelos amigáveis a PT-BR sem precisar digitar manualmente nomes de modelos e versões de pacotes repetidamente.

```python
from arcadia import models

model = models.AmadeusVerbo("3B")
```

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

## Versionamento

Este repositório versiona apenas o ambiente de execução:

- o código do pacote `arcadia`;
- o notebook de execução;
- a documentação do fluxo de trabalho de execução.

Não versione estes artefatos neste repositório:

- prompts e modelos de prompt;
- poemas gerados;
- respostas brutas de modelos;
- avaliações produzidas por modelos juízes;
- documentos derivados de saídas de modelos.

Esses artefatos dependem do prompt, do modelo e das configurações de execução, não apenas do código. Eles devem ficar em um repositório separado, preferencialmente dentro de um cofre do Obsidian.

Observe que as releases `s*` utilizam versionamento baseado em dados. Elas são mantidas apenas para preservar o histórico, mas estão descontinuadas.


[^1]: https://poemanalysis.com/definition/arcadia/
