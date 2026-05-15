"""Mem0 client setup."""

import os
import sys
from pathlib import Path

from openai import APIStatusError, OpenAI, PermissionDeniedError
from mem0 import Memory

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
CHROMA_PATH = PROJECT_ROOT / ".mem0" / "chroma"


def _load_env() -> None:
    if not ENV_FILE.exists():
        return

    try:
        from dotenv import load_dotenv

        load_dotenv(ENV_FILE, override=True)
        return
    except ImportError:
        pass

    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        os.environ[key.strip()] = value


_PLACEHOLDER_KEYS = {"", "sk-your-key-here", "your-api-key-here"}


def _require_openai_key() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key and api_key not in _PLACEHOLDER_KEYS:
        return

    raise RuntimeError(
        "OPENAI_API_KEY is missing or still a placeholder. Mem0's default "
        "config uses OpenAI for embeddings and the LLM.\n\n"
        f"Edit {ENV_FILE} and set your real key:\n"
        "  OPENAI_API_KEY=sk-..."
    )


_EMBEDDING_FALLBACKS = ("text-embedding-ada-002", "text-embedding-3-small")
_LLM_FALLBACKS = ("gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-3.5-turbo")


def _api_access_denied(exc: BaseException) -> bool:
    if isinstance(exc, (PermissionDeniedError, APIStatusError)):
        return getattr(exc, "status_code", None) in (403, 404)
    err = str(exc).lower()
    return "does not have access" in err or "model_not_found" in err


def _resolve_embedding_model(preferred: str, api_key: str) -> str:
    """Pick first embedding model the API key's OpenAI project can access."""
    candidates = [preferred] + [m for m in _EMBEDDING_FALLBACKS if m != preferred]
    client = OpenAI(api_key=api_key)

    for model in candidates:
        try:
            client.embeddings.create(input=["ping"], model=model)
            if model != preferred:
                print(
                    f"Note: project cannot use '{preferred}'; using '{model}' instead.",
                    file=sys.stderr,
                )
                print(
                    "Enable the preferred model on the same OpenAI project as this API key.",
                    file=sys.stderr,
                )
            return model
        except Exception as exc:
            if _api_access_denied(exc):
                continue
            raise

    raise RuntimeError(
        f"No embedding model available. Tried: {', '.join(candidates)}.\n\n"
        "Run: python scripts/check_openai_access.py\n"
    )


def _resolve_llm_model(preferred: str, api_key: str) -> str:
    """Pick first chat model the API key's OpenAI project can access."""
    candidates = [preferred] + [m for m in _LLM_FALLBACKS if m != preferred]
    client = OpenAI(api_key=api_key)

    for model in candidates:
        try:
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=3,
            )
            if model != preferred:
                print(
                    f"Note: project cannot use '{preferred}'; using '{model}' instead.",
                    file=sys.stderr,
                )
            return model
        except Exception as exc:
            if _api_access_denied(exc):
                continue
            raise

    raise RuntimeError(
        f"No chat/LLM model available. Tried: {', '.join(candidates)}.\n\n"
        "Mem0 needs BOTH embeddings and a chat model for memory extraction.\n\n"
        "Option A — enable chat on the embedding project:\n"
        "  Project Settings → Model access → gpt-4o-mini → new API key → .env\n\n"
        "Option B — two keys from two projects (if one has embeddings, one has chat):\n"
        "  OPENAI_API_KEY=sk-...        # project with embeddings\n"
        "  OPENAI_LLM_API_KEY=sk-...    # project with gpt-4o-mini\n\n"
        "Then run: python scripts/check_openai_access.py\n"
    )


def _llm_api_key() -> str:
    """Optional separate key when embeddings and chat live on different OpenAI projects."""
    return (
        os.getenv("OPENAI_LLM_API_KEY", "").strip()
        or os.getenv("OPENAI_API_KEY", "").strip()
    )


def _memory_config(
    embedding_model: str,
    llm_model: str,
    embed_api_key: str,
    llm_api_key: str,
) -> dict:
    # Chroma avoids Mem0's default Qdrant backend, which requires Python 3.10+.
    return {
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "firecast",
                "path": str(CHROMA_PATH),
            },
        },
        "embedder": {
            "provider": "openai",
            "config": {"model": embedding_model, "api_key": embed_api_key},
        },
        "llm": {
            "provider": "openai",
            "config": {"model": llm_model, "api_key": llm_api_key},
        },
    }


def create_memory() -> Memory:
    _load_env()
    _require_openai_key()
    embed_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    llm_api_key = _llm_api_key()
    preferred_embedding = os.getenv(
        "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
    )
    preferred_llm = os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini")
    embedding_model = _resolve_embedding_model(preferred_embedding, embed_api_key)
    llm_model = _resolve_llm_model(preferred_llm, llm_api_key)

    dual_key = llm_api_key != embed_api_key
    print(f"Using embedding: {embedding_model} | LLM: {llm_model}")
    if dual_key:
        print("Using separate API keys for embeddings vs LLM (OPENAI_LLM_API_KEY).")

    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    memory = Memory.from_config(
        _memory_config(embedding_model, llm_model, embed_api_key, llm_api_key)
    )
    active_embedding = memory.embedding_model.config.model
    active_llm = memory.llm.config.model
    if active_embedding != embedding_model:
        raise RuntimeError(
            f"Mem0 embedder model mismatch: expected '{embedding_model}', "
            f"got '{active_embedding}'."
        )
    if active_llm != llm_model:
        raise RuntimeError(
            f"Mem0 LLM model mismatch: expected '{llm_model}', got '{active_llm}'."
        )
    return memory
