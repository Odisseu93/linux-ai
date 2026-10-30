#!/usr/bin/env python
"""
Linux AI - Local Linux assistant powered by llama.cpp.
"""

import os
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------
# Configuration
# --------------------------------------------------

LLAMA = Path(
    os.getenv(
        "LINUX_AI_LLAMA",
        str(Path.home() / "llama.cpp/build/bin/llama-cli")
    )
).expanduser()

MODEL = Path(
    os.getenv(
        "LINUX_AI_MODEL",
        str(Path.home() / "IA/modelos/qwen2.5-0.5b.gguf")
    )
).expanduser()

CONTEXT = int(os.getenv("LINUX_AI_CONTEXT", "1024"))
MAX_TOKENS = int(os.getenv("LINUX_AI_MAX_TOKENS", "256"))
THREADS = int(os.getenv("LINUX_AI_THREADS", "2"))
MAX_PIPE_CHARS = int(os.getenv("LINUX_AI_MAX_PIPE_CHARS", "12000"))
MAX_HISTORY = 2
TIMEOUT = 600

# --------------------------------------------------
# Language configuration
# --------------------------------------------------

LANGUAGE_ALIASES = {
    "pt": "pt-BR",
    "pt-br": "pt-BR",
    "portuguese": "pt-BR",
    "en": "en-US",
    "en-us": "en-US",
    "english": "en-US",
}

LANGUAGE = LANGUAGE_ALIASES.get(
    os.getenv("LINUX_AI_LANGUAGE", "pt-BR").strip().lower()
)

if LANGUAGE is None:
    LANGUAGE = "pt-BR"
    print(
        "Warning: Unsupported language. "
        "Falling back to Brazilian Portuguese."
    )

SYSTEM_PROMPTS = {
    "pt-BR": """
Você é Linux AI, um assistente especialista em Linux Ubuntu.

Responda sempre em português brasileiro.

Suas responsabilidades:
- Explicar comandos Linux.
- Diagnosticar erros.
- Criar e explicar scripts Bash.
- Explicar permissões, usuários e grupos.
- Auxiliar na administração de processos e serviços.
- Ajudar na administração do Ubuntu.

Regras:
1. Explique o objetivo de cada comando.
2. Apresente exemplos práticos.
3. Explique os parâmetros utilizados.
4. Alerte sobre comandos destrutivos.
5. Nunca execute comandos.
6. Não invente opções ou parâmetros.
7. Se não souber, admita.
8. Diferencie fatos de hipóteses.

Use respostas claras, organizadas e objetivas.
""",

    "en-US": """
You are Linux AI, an assistant specialized in Ubuntu Linux.

Always respond in American English.

Your responsibilities:
- Explain Linux commands.
- Troubleshoot system errors.
- Create and explain Bash scripts.
- Explain permissions, users, and groups.
- Help manage processes and services.
- Assist with Ubuntu system administration.

Rules:
1. Explain the purpose of every command.
2. Provide practical examples.
3. Explain command-line options and parameters.
4. Warn about destructive commands.
5. Never execute commands.
6. Never invent command options or parameters.
7. Admit when you do not know something.
8. Distinguish facts from hypotheses.

Keep answers clear, organized, and concise.
"""
}

UI = {
    "pt-BR": {
        "title": "LINUX AI ASSISTANT",
        "subtitle": "Assistente Linux Offline",
        "execution": "Execução",
        "local": "Local",
        "help_hint": "Digite /ajuda para ver os comandos.",
        "exit_hint": "Digite /sair para encerrar.",
        "thinking": "pensando...",
        "analyzing": "analisando entrada recebida...",
        "you": "Você",
        "assistant": "Linux AI",
        "goodbye": "Até logo!",
        "help": """
Comandos disponíveis:

/ajuda   - Exibe esta ajuda
/limpar  - Limpa o histórico
/sair    - Encerra o assistente

Faça perguntas sobre Linux normalmente.
""",
        "history_cleared": "Histórico apagado.",
        "model_missing": "Modelo não encontrado",
        "llama_missing": "Executável llama-cli não encontrado",
        "empty_response": "O modelo não retornou uma resposta.",
        "timeout": "Tempo limite excedido.",
        "pipe_too_large": "Entrada do pipe excede o limite permitido.",
        "model_error": "Erro ao executar o modelo:",
        "interrupt": "Use /sair para encerrar."
    },

    "en-US": {
        "title": "LINUX AI ASSISTANT",
        "subtitle": "Offline Linux Assistant",
        "execution": "Execution",
        "local": "Local",
        "help_hint": "Type /help to see available commands.",
        "exit_hint": "Type /exit to quit.",
        "thinking": "thinking...",
        "analyzing": "analyzing piped input...",
        "you": "You",
        "assistant": "Linux AI",
        "goodbye": "Goodbye!",
        "help": """
Available commands:

/help   - Display this help
/clear  - Clear conversation history
/exit   - Exit the assistant

Ask Linux-related questions normally.
""",
        "history_cleared": "Conversation history cleared.",
        "model_missing": "Model not found",
        "llama_missing": "llama-cli executable not found",
        "empty_response": "The model returned an empty response.",
        "timeout": "Request timed out.",
        "pipe_too_large": "Piped input exceeds the allowed size.",
        "model_error": "Error running the model:",
        "interrupt": "Type /exit to quit."
    }
}

TEXT = UI[LANGUAGE]
SYSTEM = SYSTEM_PROMPTS[LANGUAGE]


# --------------------------------------------------
# User interface
# --------------------------------------------------

def banner():
    print("=" * 48)
    print(f"             {TEXT['title']}")
    print(f"             {TEXT['subtitle']}")
    print("=" * 48)
    print(f"Model: {MODEL.name}")
    print(f"{TEXT['execution']}: {TEXT['local']}")
    print(f"Language: {LANGUAGE}")
    print(TEXT["help_hint"])
    print(TEXT["exit_hint"])
    print("=" * 48)


def show_help():
    print(TEXT["help"])


# --------------------------------------------------
# Input handling
# --------------------------------------------------

def read_pipe():
    """Read piped stdin, if available."""

    if sys.stdin.isatty():
        return None

    data = sys.stdin.read(MAX_PIPE_CHARS + 1)

    if len(data) > MAX_PIPE_CHARS:
        raise ValueError(TEXT["pipe_too_large"])

    return data.strip() or None


# --------------------------------------------------
# AI inference
# --------------------------------------------------

def ask_ai(question, history):
    """Send a question to llama.cpp and return the response."""

    conversation = ""

    for user, answer in history:
        if LANGUAGE == "pt-BR":
            conversation += (
                f"\nPergunta anterior: {user}\n"
                f"Resposta anterior: {answer}\n"
            )
        else:
            conversation += (
                f"\nPrevious question: {user}\n"
                f"Previous answer: {answer}\n"
            )

    if LANGUAGE == "pt-BR":
        current_prompt = (
            f"\nPergunta atual: {question}\n"
            "Responda à pergunta atual."
        )
    else:
        current_prompt = (
            f"\nCurrent question: {question}\n"
            "Answer the current question."
        )

    prompt = conversation + current_prompt

    command = [
        str(LLAMA),
        "-m", str(MODEL),
        "-c", str(CONTEXT),
        "-t", str(THREADS),
        "-b", "32",
        "-ub", "16",
        "-n", str(MAX_TOKENS),
        "--no-display-prompt",
        "--no-show-timings",
        "-sys", SYSTEM,
        "-p", prompt
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT
        )

        if result.returncode != 0:
            print(f"\n{TEXT['model_error']}")
            print(result.stderr[-2000:])
            return None

        answer = result.stdout.strip()

        if not answer:
            print(TEXT["empty_response"])
            return None

        return answer

    except subprocess.TimeoutExpired:
        print(TEXT["timeout"])
        return None

    except OSError as error:
        print(f"{TEXT['model_error']} {error}")
        return None


# --------------------------------------------------
# Main application
# --------------------------------------------------

def main():

    if not LLAMA.is_file():
        print(f"{TEXT['llama_missing']}: {LLAMA}")
        sys.exit(1)

    if not MODEL.is_file():
        print(f"{TEXT['model_missing']}: {MODEL}")
        sys.exit(1)

    history = []

    banner()

    # Handle piped input
    try:
        piped_data = read_pipe()
    except ValueError as error:
        print(error)
        sys.exit(1)

    if piped_data:
        if LANGUAGE == "pt-BR":
            question = (
                "Analise o seguinte conteúdo recebido pelo terminal. "
                "Explique o que significa, identifique possíveis problemas "
                "e sugira soluções seguras:\n\n"
                + piped_data
            )
        else:
            question = (
                "Analyze the following content received from the terminal. "
                "Explain what it means, identify potential problems, "
                "and suggest safe solutions:\n\n"
                + piped_data
            )

        print(f"\n{TEXT['assistant']}: {TEXT['analyzing']}\n")

        answer = ask_ai(question, history)

        if answer:
            print(f"{TEXT['assistant']}:\n")
            print(answer)

        return

    # Interactive mode
    while True:
        try:
            question = input(f"\n{TEXT['you']}: ").strip()

            if not question:
                continue

            command_aliases = {
                "/ajuda": "/help",
                "/limpar": "/clear",
                "/sair": "/exit"
            }

            command = command_aliases.get(
                question.lower(),
                question.lower()
            )

            if command == "/exit":
                print(f"\n{TEXT['assistant']}: {TEXT['goodbye']}")
                break

            if command == "/help":
                show_help()
                continue

            if command == "/clear":
                history.clear()
                print(TEXT["history_cleared"])
                continue

            print(f"\n{TEXT['assistant']}: {TEXT['thinking']}\n")

            answer = ask_ai(question, history)

            if answer:
                print(f"{TEXT['assistant']}:\n")
                print(answer)

                history.append((question, answer))
                history = history[-MAX_HISTORY:]

        except KeyboardInterrupt:
            print(f"\n\n{TEXT['interrupt']}")

        except EOFError:
            print(f"\n{TEXT['goodbye']}")
            break


if __name__ == "__main__":
    main()

