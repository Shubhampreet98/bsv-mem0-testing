#!/usr/bin/env python3
"""Test which OpenAI models your .env API key(s) can actually call."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from firecast.client import ENV_FILE, _load_env, _llm_api_key  # noqa: E402
from openai import OpenAI  # noqa: E402

EMBEDDING_MODELS = [
    "text-embedding-3-small",
    "text-embedding-ada-002",
]
CHAT_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1-mini",
    "gpt-3.5-turbo",
]


def _test(client: OpenAI, kind: str, model: str) -> bool:
    try:
        if kind == "embedding":
            client.embeddings.create(input=["test"], model=model)
        else:
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=3,
            )
        print(f"  OK   {model}")
        return True
    except Exception as exc:
        print(f"  FAIL {model}")
        print(f"       {exc}")
        return False


def _check_key(label: str, key: str) -> tuple[int, int]:
    print(f"\n{label} ({key[:12]}...{key[-4:]})")
    client = OpenAI(api_key=key)
    print("  Embeddings:")
    emb_ok = sum(_test(client, "embedding", m) for m in EMBEDDING_MODELS)
    print("  Chat:")
    chat_ok = sum(_test(client, "chat", m) for m in CHAT_MODELS)
    return emb_ok, chat_ok


def main() -> None:
    _load_env()
    embed_key = os.getenv("OPENAI_API_KEY", "")
    llm_key = _llm_api_key()
    if not embed_key:
        print("No OPENAI_API_KEY in .env")
        sys.exit(1)

    print(f"Env file: {ENV_FILE}")
    emb_ok, chat_ok = _check_key("OPENAI_API_KEY", embed_key)

    if llm_key != embed_key:
        _, llm_chat_ok = _check_key("OPENAI_LLM_API_KEY", llm_key)
        chat_ok = max(chat_ok, llm_chat_ok)

    print(f"\nSummary: embeddings OK on main key: {emb_ok > 0}; chat OK (any key): {chat_ok > 0}")
    if emb_ok and chat_ok:
        print("Ready for: python firecast_test.py")
        return
    if emb_ok and not chat_ok:
        print(
            "\n>>> Add OPENAI_LLM_API_KEY with a key from a project that has gpt-4o-mini,\n"
            "    or enable chat models on your embedding project."
        )
    sys.exit(1)


if __name__ == "__main__":
    main()
