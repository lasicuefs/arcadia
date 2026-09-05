<p align="right">
<a href="./GUIDE.pt-BR">Leia em português</a>
</p>

<div align="center">

# ✦ Arcadia for Everyone ✦

> This guide is for anyone who wants to use Arcadia without programming or machine learning experience.

</div>

<p align="center">
———————————————— 🙡 ————————————————
</p>

## Before you begin

To follow this guide, you only need:

- A Google account
- An internet connection
- A modern web browser (Chrome, Firefox, Edge, or Safari)

You do **not** need to install Python, Git, or any other software.

## What is Arcadia?

Arcadia is an application that lets you chat with Artificial Intelligence (AI) models.

These AI models can run:

- **In Google's cloud** using Google Colab (recommended)
- **On your own computer**

For most users, Google Colab is the easiest option because nothing needs to be installed.

## Where does Arcadia run?

Arcadia supports two ways of running AI models.

### Google Colab (Recommended)

Google Colab runs everything on Google's cloud.

This is the easiest option because:

- Nothing needs to be installed.
- It runs directly in your web browser.
- It works on most computers.
- Google provides the computing resources.

### Your own computer (Advanced)

Running Arcadia locally gives you more control, but usually requires:

- Python
- Git
- A reasonably powerful computer
- Basic familiarity with the command line

If this is your first time using Arcadia, we recommend using **Google Colab**.


# Running Arcadia

## 1. Open the notebook

Google Colab uses **notebooks**.

A notebook is a document containing explanations and pieces of code that you can execute one at a time. Each piece is called a **cell**.

Open the Arcadia notebook:

**https://colab.research.google.com/github/lasicuefs/arcadia/blob/main/play.ipynb**

You'll see something similar to this:

![Google Colab](./docs/images/google_colab.png)

## 2. Prepare Google Colab

Before running Arcadia, you'll need to prepare the notebook.

### Choose a runtime

Google Colab provides a temporary computer called a **runtime**.

Arcadia runs inside this runtime instead of your own computer.

For most users, **T4 GPU** provides the best balance between speed and availability.

### Connect to a T4 GPU

This is the easiest way to get started.

![Connect T4](./docs/images/connect_to_t4.png)

### Choose another runtime (Optional)

If you prefer another runtime:

1. Click the menu next to **Connect**.
2. Select **Change runtime type**.

![Runtime menu](./docs/images/change_runtime.png)

Then:

1. Select the runtime you want.
2. Leave the remaining options unchanged.
3. Click **Save**.

![Available runtimes](./docs/images/available_runtimes.png)

> [!NOTE]
>
> Google Colab sessions are temporary.
> If your session expires, simply reconnect the runtime and continue.

## 3. Install Arcadia

Run the first code cell.

This downloads Arcadia and its required libraries into the temporary Google Colab environment.

**Nothing is permanently installed on your computer.**

Click **Run** (▶).

![Installing Arcadia](./docs/images/install_arcadia.png)

## 4. Configure the output file

Arcadia automatically saves your conversations to an output file.

You may choose the folder where your conversations will be stored. But this will be stored into `outputs/` by default.

![Configure output](./docs/images/configure_output.png)


## 5. Configure a Hugging Face Token (Optional)

> [!TIP]
>
> This step is optional.
>
> Arcadia works without a Hugging Face token, but model downloads may be slower.

### Create a token

1. Open the Hugging Face Access Tokens page:
   https://huggingface.co/settings/tokens

2. Click **Create new token**.

![Access Tokens](./docs/images/access_token.png)

3. Give your token a meaningful name, such as **Arcadia**.
4. Click **Create token**.
5. Copy the generated token.

![Create token](./docs/images/arcadia_token.png)

### Configure the token in Google Colab

Open the notebook again.

1. Open **Secrets** (🔑) from the left sidebar.
2. Enable **Notebook Access**.
3. Create a secret named **HF_TOKEN**.
4. Paste your Hugging Face token into the **Value** field.

![Paste token](./docs/images/paste_hf_token.png)

# Choosing an AI model

Before chatting with the AI, you'll need to choose which model to use.
Arcadia includes several models with different sizes and capabilities.

## Recommended models

| Model | Default Size |
|---------|--------------|
| Gaia | `4B` |
| AmadeusVerbo | `3B` |
| Tucano | `2.4B` |
| TeenyTinyLlama | `460M` |

In general:

- Smaller models download faster and use less memory.
- Larger models usually generate better responses but take longer to download.

## Simplest option

Most users can simply write:

### Gaia

```python
from arcadia import models

model = models.Gaia()
```

### AmadeusVerbo

```python
from arcadia import models

model = models.AmadeusVerbo()
```

### Tucano

```python
from arcadia import models

model = models.Tucano()
```

### TeenyTinyLlama

```python
from arcadia import models

model = models.TeenyTinyLlama()
```

Arcadia automatically selects the recommended size.

## Choosing another size (Advanced)

If you want a different model size, specify it manually.

```python
from arcadia import models

model = models.AmadeusVerbo("7B")
```

> [!TIP]
>
> The size must be one of the sizes supported by the selected model.

## Downloading the model

Click **Run** (▶).

The first time you run this cell, Arcadia will:

1. Read the table to see which model and size you want.
2. Prepare it for use.
3. Start the conversation.

Depending on your internet connection and the selected model, this may take several minutes.

![Selecting model](./docs/images/select_model.png)

# Chatting with the model

## Asking your first question

To ask a question:

1. Replace the text inside the quotation marks.
2. Click **Run** (▶).
3. Wait for the answer to appear below the cell.

![First prompt](./docs/images/ask_mode.png)

## Continuing the conversation

If you want, you may chat with the model naturally.

In the **Chat** section, arcadia remembers previous messages, allowing you to ask follow-up questions without repeating the earlier conversation.

Simply:

1. Click **Run** (▶).
2. Type your first message.
3. Read the history of the text.
4. Write your next message.

![Chat mode](./docs/images/chat_mode.png)

To end the conversation:

- Type `quit`, or
- Type `exit`, or
- Click **Stop** (⏹).

# Saving your conversations

Your conversations are saved automatically.

To download them:

1. Open **Files** (📁).
2. Open the **outputs** folder.
3. Double-click the desired file.
4. Click **⋮** → **Download**.

![Download output](./docs/images/capturing_output.png)

# Next steps

Now that Arcadia is running, you can:

- Try different AI models.
- Ask questions in natural language.
- Compare model responses.
- Save your conversations.
- Experiment with different prompts.

As you become more familiar with Arcadia, you can explore advanced features and even run models on your own computer.

---

# Glossary

**Cell**
: A block inside a notebook. Some cells contain explanations, while others contain code that you can run.

**Cloud**
: Computers running on the internet instead of your own device.

**Google Colab**
: A free cloud service from Google that lets you run Python code directly in your web browser.

**Large Language Model (LLM)**
: A type of Artificial Intelligence trained to understand and generate human language. ChatGPT, Claude, Gemini, Llama, and Gaia are examples of LLMs.

**Notebook**
: An interactive document that combines text, code, and results in one place.

**Open Source**
: Software whose source code is publicly available and can be studied, modified, and redistributed.

**Prompt**
: The text or question that you send to the AI.

**Runtime**
: The temporary computer where your notebook runs in Google Colab.

**GPU**
: A specialized processor that makes AI models run much faster than a regular CPU.


<div align="center">

**Arcadia**<br>
*Um portal poético para explorar modelos de linguagem dentro do LASIC.*

</div>

<p align="center">🙡 ✦ 🙡</p>
