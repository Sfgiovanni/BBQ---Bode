"""Language-matched prompt rendering for supported model prompt styles."""

from typing import Any, Dict


COPY = {
    "pt": {
        "instruction": "Responda à pergunta de múltipla escolha apenas com A, B ou C, sem explicação.",
        "context": "Contexto",
        "question": "Pergunta",
        "options": "Opções",
        "alpaca_prefix": "Abaixo está uma instrução que descreve uma tarefa, juntamente com uma entrada que fornece mais contexto. Escreva uma resposta que complete adequadamente o pedido.",
        "instruction_header": "Instrução",
        "input_header": "Entrada",
        "answer_header": "Resposta",
    },
    "en": {
        "instruction": "Answer the multiple-choice question with A, B, or C only, without explanation.",
        "context": "Context",
        "question": "Question",
        "options": "Options",
        "alpaca_prefix": "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.",
        "instruction_header": "Instruction",
        "input_header": "Input",
        "answer_header": "Response",
    },
}


def _body(example: Dict[str, Any]) -> str:
    copy = COPY[example["language"]]
    return """{context_header}:
{context}

{question_header}:
{question}

{options_header}:
A) {option_A}
B) {option_B}
C) {option_C}""".format(
        context_header=copy["context"],
        context=example["context"],
        question_header=copy["question"],
        question=example["question"],
        options_header=copy["options"],
        option_A=example["option_A"],
        option_B=example["option_B"],
        option_C=example["option_C"],
    )


def render_prompt(example: Dict[str, Any], prompt_style: str, tokenizer: Any = None) -> str:
    """Render an Alpaca, tokenizer-chat, or simple causal prompt."""
    if example["language"] not in COPY:
        raise ValueError("Unsupported language: {}".format(example["language"]))
    copy = COPY[example["language"]]
    body = _body(example)
    if prompt_style == "alpaca":
        return """{prefix}

### {instruction_header}:
{instruction}

### {input_header}:
{body}

### {answer_header}:""".format(
            prefix=copy["alpaca_prefix"],
            instruction_header=copy["instruction_header"],
            instruction=copy["instruction"],
            input_header=copy["input_header"],
            body=body,
            answer_header=copy["answer_header"],
        )
    if prompt_style == "simple":
        return "{}\n\n{}\n\n{}:".format(copy["instruction"], body, copy["answer_header"])
    if prompt_style == "chat_template":
        if tokenizer is None or not hasattr(tokenizer, "apply_chat_template"):
            raise ValueError("chat_template requires a compatible tokenizer")
        messages = [{"role": "user", "content": copy["instruction"] + "\n\n" + body}]
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    raise ValueError("Unsupported prompt style: {}".format(prompt_style))
