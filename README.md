# Linux AI

### Local intelligence for Linux, without the cloud.

A lightweight, terminal-based AI assistant for Linux system administration, powered by [llama.cpp](<https://github.com/ggml-org/llama.cpp>).

Linux AI helps users understand Linux commands, troubleshoot system issues, and learn system administration using locally hosted language models.

It runs directly on your machine without requiring cloud APIs, external AI services, or subscription fees.

---

## Overview

Linux AI was created to bring local artificial intelligence to Linux users, including those running older computers with limited hardware resources.

The project prioritizes:

- Local and offline AI inference.
- Low resource consumption.
- Terminal-only interaction.
- Simplicity and portability.
- Practical Linux administration assistance.
- User control and system security.

The assistant does not automatically execute commands. It provides explanations, suggestions, and troubleshooting guidance while leaving system operations under the user's control.

## Features

### Implemented

- [x] Local AI inference through llama.cpp.
- [x] GGUF model support.
- [x] Interactive terminal interface.
- [x] Brazilian Portuguese as the default language.
- [x] American English language support.
- [x] Language selection through environment variables.
- [x] Conversation history during the current session.
- [x] Built-in terminal commands.
- [x] Standard input and pipe support.
- [x] Configurable model location.
- [x] Configurable llama.cpp executable.
- [x] Configurable inference parameters.
- [x] No external Python dependencies.

### Planned

- [ ] Automatic system information collection.
- [ ] Linux system diagnostics.
- [ ] Persistent model loading between requests.
- [ ] Advanced log analysis.
- [ ] Improved conversation context management.
- [ ] Structured troubleshooting reports.
- [ ] Persistent conversation history.
- [ ] Additional language support.

## Architecture

Linux AI uses a simple architecture:

text

```
              User
                |
                v
          Linux AI CLI
             Python
                |
                v
            llama.cpp
             llama-cli
                |
                v
          GGUF Language Model
                |
                v
            AI Response
```

Python handles the terminal interface, configuration, conversation history, and model invocation.

llama.cpp handles local language model inference.

## Requirements

### Software

- Linux operating system.
- Python 3.
- Python venv module.
- llama.cpp.
- A compatible GGUF language model.
- Git (for cloning the repository).

### Hardware

The project was initially developed and tested on:

| Component | Specification |
| --- | --- |
| Computer | HP ProBook 6450b |
| CPU | Intel Core i5 M 560 |
| CPU cores | 2 physical / 4 threads |
| RAM | 4 GB DDR3 |
| GPU | Integrated Intel graphics |
| Storage | Approximately 298 GB |
| OS | Ubuntu Linux |

The original development CPU does not support AVX instructions.

For this reason, llama.cpp must be compiled using compatible CPU settings.

Newer processors may use different compilation options.

## Installation

### 1\. Install system dependencies

On Ubuntu:

bash

```
sudo apt update

sudo apt install -y \
    git \
    build-essential \
    cmake \
    libopenblas-dev \
    python3 \
    python3-venv \
    wget
```

### 2\. Clone the repository

bash

```
git clone https://github.com/Odisseu93/linux-ai.git

cd linux-ai
```

### 3\. Create a Python virtual environment

bash

```
python3 -m venv .venv
```

Activate it:

bash

```
source .venv/bin/activate
```

Update pip:

bash

```
python -m pip install --upgrade pip
```

### 4\. Install Python dependencies

bash

```
pip install -r requirements.txt
```

Linux AI currently uses only Python standard-library modules.

No additional Python packages are required.

### 5\. Install llama.cpp

Clone the official repository:

bash

```
git clone https://github.com/ggml-org/llama.cpp
```

Compile it:

bash

```
cd llama.cpp
```

For older processors without AVX support:

bash

```
cmake -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DGGML_NATIVE=OFF \
    -DGGML_SSE42=ON \
    -DGGML_AVX=OFF \
    -DGGML_AVX2=OFF \
    -DGGML_AVX_VNNI=OFF \
    -DGGML_AVX512=OFF \
    -DGGML_BMI2=OFF \
    -DGGML_FMA=OFF \
    -DGGML_F16C=OFF \
    -DGGML_OPENMP=OFF
```

Build:

bash

```
cmake --build build --config Release -j1
```

Return to the Linux AI directory:

bash

```
cd ..
```

**Note:** These compilation settings are intended for the original development hardware. Other CPUs may benefit from different configurations.

### 6\. Download a language model

The initial recommended model is:

**Qwen2.5 0.5B Instruct — Q4\_K\_M GGUF**

Create the model directory:

bash

```
mkdir -p ~/IA/modelos
```

Download:

bash

```
wget -O ~/IA/modelos/qwen2.5-0.5b.gguf \
"https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf"
```

Model repository:

[https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF](<https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF>)

The model is distributed separately from this project.

Please check the model repository for licensing and usage terms.

## Configuration

Linux AI supports environment variables for configuration.

| Variable | Default | Description |
| --- | --- | --- |
| `LINUX_AI_LANGUAGE` | `pt-BR` | Assistant language |
| `LINUX_AI_LLAMA` | `~/llama.cpp/build/bin/llama-cli` | llama.cpp executable |
| `LINUX_AI_MODEL` | `~/IA/modelos/qwen2.5-0.5b.gguf` | GGUF model path |
| `LINUX_AI_CONTEXT` | `1024` | Context size |
| `LINUX_AI_MAX_TOKENS` | `256` | Maximum generated tokens |
| `LINUX_AI_THREADS` | `2` | CPU threads |
| `LINUX_AI_MAX_PIPE_CHARS` | `12000` | Maximum piped input size |

### Language configuration

Brazilian Portuguese is the default language.

Run in Portuguese:

bash

```
python linux-ai.py
```

Run in American English:

bash

```
LINUX_AI_LANGUAGE=en-US python linux-ai.py
```

Explicitly select Brazilian Portuguese:

bash

```
LINUX_AI_LANGUAGE=pt-BR python linux-ai.py
```

Short aliases are also supported:

bash

```
LINUX_AI_LANGUAGE=en python linux-ai.py

LINUX_AI_LANGUAGE=pt python linux-ai.py
```

The selected language changes both the terminal interface and the assistant's system prompt.

### Custom model location

bash

```
export LINUX_AI_MODEL="$HOME/models/my-model.gguf"
```

### Custom llama.cpp executable

bash

```
export LINUX_AI_LLAMA="$HOME/llama.cpp/build/bin/llama-cli"
```

### Inference settings

For example:

bash

```
export LINUX_AI_CONTEXT=1024
export LINUX_AI_MAX_TOKENS=256
export LINUX_AI_THREADS=2
```

Adjust these values according to your available hardware resources.

## Usage

Activate the virtual environment:

bash

```
source .venv/bin/activate
```

Start Linux AI:

bash

```
python linux-ai.py
```

### Interactive mode

Example:

text

```
================================================
             LINUX AI ASSISTANT
             Assistente Linux Offline
================================================

Model: qwen2.5-0.5b.gguf
Execution: Local
Language: pt-BR

Você: Como verificar o espaço em disco?

Linux AI:

Use o comando:

df -h

Ele apresenta o espaço utilizado e disponível
em cada sistema de arquivos.
```

### Built-in commands

| Command | Description |
| --- | --- |
| `/ajuda` | Display help in Portuguese |
| `/help` | Display help in English |
| `/limpar` | Clear conversation history |
| `/clear` | Clear conversation history |
| `/sair` | Exit Linux AI |
| `/exit` | Exit Linux AI |

## Piped Input

Linux AI can receive information through standard input.

This allows it to become part of traditional Unix pipelines.

### Examples

Analyze disk usage:

bash

```
df -h | python linux-ai.py
```

Analyze memory usage:

bash

```
free -h | python linux-ai.py
```

Analyze failed systemd services:

bash

```
systemctl --failed | python linux-ai.py
```

Analyze recent system errors:

bash

```
journalctl -p err -n 30 | python linux-ai.py
```

Analyze kernel messages:

bash

```
dmesg | python linux-ai.py
```

When piped input is detected, Linux AI analyzes the received content instead of starting an interactive session.

The current implementation includes an input size limit to help prevent excessive memory consumption.

**Note:** The input character limit does not guarantee that the content fits within the model's context window.

## Security

Linux AI is designed as an advisory tool.

It does not automatically execute commands generated by the model.

The user remains responsible for reviewing and executing any suggested commands.

Important security considerations:

- AI-generated commands may be incorrect.
- Destructive operations must be reviewed carefully.
- Administrative commands may require elevated privileges.
- System logs may contain sensitive information.
- Piped input must be treated as untrusted data.
- Always review commands before executing them.

Linux AI is not intended to replace system administration knowledge, backups, or security practices.

## Performance

The original development machine has limited hardware resources.

The initial inference configuration is intentionally conservative:

| Parameter | Value |
| --- | --- |
| Context | 1024 tokens |
| CPU threads | 2 |
| Batch size | 32 |
| Micro-batch size | 16 |
| Maximum output | 256 tokens |

The current implementation starts a new llama.cpp process for each question.

Persistent model loading is planned to reduce startup latency and improve the interactive experience.

## Project Structure

text

```
linux-ai/
├── linux-ai.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
└── .venv/
```

The `.venv/` directory is local and must not be committed to Git.

Model files must also remain outside the repository.

## Roadmap

### Core functionality

- [x] Local inference.
- [x] Terminal interface.
- [x] Brazilian Portuguese support.
- [x] American English support.
- [x] Conversation history.
- [x] Built-in commands.
- [x] Piped input.
- [x] Configurable model path.
- [x] Configurable llama.cpp path.

### System integration

- [ ] RAM and swap inspection.
- [ ] Disk usage analysis.
- [ ] Process monitoring.
- [ ] systemd service inspection.
- [ ] Kernel information collection.
- [ ] Network and port inspection.

### Performance

- [ ] Persistent model loading.
- [ ] Improved context management.
- [ ] Reduced inference startup latency.
- [ ] Memory usage optimization.

### Diagnostics

- [ ] Interactive diagnostic mode.
- [ ] Advanced log analysis.
- [ ] Error classification.
- [ ] Structured troubleshooting reports.
- [ ] Safe command recommendations.

### User experience

- [ ] Persistent conversation history.
- [ ] Improved terminal formatting.
- [ ] External configuration file.
- [ ] Additional language support.

## Contributing

Contributions, suggestions, and bug reports are welcome.

When contributing, please consider:

- Compatibility with older CPUs.
- Low memory consumption.
- Offline operation.
- Terminal-only interaction.
- Safe handling of system information.
- Maintaining existing functionality.

## License
[GNU General Public License v3.0](LICENSE)

Third-party dependencies and language models retain their respective licenses.

## Acknowledgments

- [llama.cpp](<https://github.com/ggml-org/llama.cpp>) — Local LLM inference engine.
- Qwen — Qwen2.5 language model family.
- [Hugging Face](<https://huggingface.co/>) — Model hosting and distribution.

---

**Linux AI — Local intelligence for Linux, without the cloud.**
