#!/usr/bin/env python3
"""
Ameena Offline Demo — Gemma 4 for Rural Central Asian Schools
Runs locally on MacBook / Raspberry Pi / Android (via Termux) using llama.cpp.
No internet required. No fine-tuning required.

Submission for the Kaggle Gemma 4 Good Hackathon.
  Tracks: Digital Equity & Inclusivity + Future of Education + llama.cpp Special Prize
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    from llama_cpp import Llama
except ImportError:
    print("ERROR: llama-cpp-python is not installed.", file=sys.stderr)
    print("Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


# Recommended file: gemma-4-4b-it-Q4_K_M.gguf (~2.5 GB), downloaded by the user.
MODEL_PATH = os.getenv(
    "GEMMA4_MODEL_PATH",
    "./gemma-4-4b-it-Q4_K_M.gguf",
)

DEFAULT_PROMPT = (
    "Шумо муаллими математика ҳастед. "
    "Ба хонандаи синфи 5-ум тавсиф кунед, ки чӣ гуна касрҳоро ҷамъ кардан мумкин аст. "
    "Бо забони тоҷикӣ ҷавоб диҳед."
)


def load_model(model_path: str) -> Llama:
    """Load Gemma 4 with CPU-friendly defaults that work on $100 hardware."""
    if not Path(model_path).is_file():
        print(f"ERROR: model file not found at {model_path}", file=sys.stderr)
        print(
            "Download a GGUF build of Gemma 4 (e.g. gemma-4-4b-it-Q4_K_M.gguf) "
            "and either place it next to inference.py or set GEMMA4_MODEL_PATH.",
            file=sys.stderr,
        )
        sys.exit(2)

    return Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=4,
        n_gpu_layers=0,
        verbose=False,
    )


def generate(llm: Llama, prompt: str, max_tokens: int = 512) -> str:
    """Generate a response using Gemma 4's chat template."""
    formatted = (
        "<bos><start_of_turn>user\n"
        f"{prompt}\n"
        "<end_of_turn><start_of_turn>model\n"
    )
    output = llm(
        formatted,
        max_tokens=max_tokens,
        stop=["<end_of_turn>", "<eos>"],
        temperature=0.3,
        top_p=0.9,
    )
    return output["choices"][0]["text"].strip()


def read_prompt(arg: str | None) -> str:
    """Accept either a literal prompt or a path to a .txt file."""
    if not arg:
        return DEFAULT_PROMPT
    candidate = Path(arg)
    if candidate.is_file():
        return candidate.read_text(encoding="utf-8").strip()
    return arg


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ameena offline tutor (Gemma 4 + llama.cpp)",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default=None,
        help=(
            "Prompt text, OR a path to a .txt file (e.g. "
            "sample_prompts/tajik_math.txt). Default: Tajik fractions question."
        ),
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Maximum tokens to generate (default: 512).",
    )
    parser.add_argument(
        "--model",
        default=MODEL_PATH,
        help=f"Path to GGUF model (default: {MODEL_PATH}).",
    )
    args = parser.parse_args()

    prompt = read_prompt(args.prompt)

    print("Ameena Offline Tutor — Gemma 4")
    print(f"Model:  {args.model}")
    print(f"Prompt: {prompt}\n")
    print("Answer:")
    print("-" * 40)

    llm = load_model(args.model)
    response = generate(llm, prompt, max_tokens=args.max_tokens)
    print(response)
    return 0


if __name__ == "__main__":
    sys.exit(main())
