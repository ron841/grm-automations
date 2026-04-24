"""Phase 4-new LLM helper — thin wrapper over the Anthropic SDK.

Editorial fields across Gates B-E (personaReason,
signatureMicroInteractionReason, microInteractionsReason, *Copy
fields, italicSelections, pullQuotes, eyebrowDeployments,
aboutStory narrativeBlocks) are authored via LLM calls made through
this module.

Public API (3 symbols):

  MODEL_EDITORIAL       default model for editorial authoring
  MODEL_DETERMINISTIC   lower-cost model for deterministic lookups
  call_editorial(...)   single-turn messages.create call; returns text

Prompt templates live in calling modules (select_persona.py,
resolve_signatures.py, etc.) per Design's Gate B direction. This
module does not template. It does not retry. It does not cache.
Keep it thin and inspectable.
"""

import os
from typing import Optional

import anthropic


MODEL_EDITORIAL = "claude-opus-4-7"
MODEL_DETERMINISTIC = "claude-haiku-4-5-20251001"


_client: Optional[anthropic.Anthropic] = None


def _get_client() -> anthropic.Anthropic:
    """Lazily instantiate and cache the Anthropic client.

    Sequential orchestrator — thread-safety not required at
    Phase 4-new execution level.
    """
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY environment variable is required "
                "for Phase 4-new editorial LLM calls. Set via:\n"
                "  export ANTHROPIC_API_KEY=sk-ant-..."
            )
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def call_editorial(
    system_prompt: str,
    user_prompt: str,
    model: str = MODEL_EDITORIAL,
    max_tokens: int = 500,
    temperature: float = 1.0,
) -> str:
    """Make a single-turn Anthropic API call; return assistant response text.

    Parameters
    ----------
    system_prompt
        System prompt passed to messages.create as the `system` field.
    user_prompt
        User message content passed as a single user-role message.
    model
        Anthropic model ID. Defaults to MODEL_EDITORIAL.
    max_tokens
        Max tokens for the response.
    temperature
        Sampling temperature.

    Returns
    -------
    str
        Text content of the first content block in the assistant response.

    Raises
    ------
    RuntimeError
        ANTHROPIC_API_KEY missing or empty; response carries an empty
        content list; or the first content block is not a text block.
    anthropic.APIError
        Subclasses surfaced to caller. Retry policy belongs to calling
        modules per helper's thin-wrapper scope.
    """
    client = _get_client()
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        temperature=temperature,
    )
    if not response.content:
        raise RuntimeError(
            "Anthropic response carried empty content list "
            f"(stop_reason={getattr(response, 'stop_reason', None)})"
        )
    first = response.content[0]
    text = getattr(first, "text", None)
    if text is None:
        block_type = getattr(first, "type", type(first).__name__)
        raise RuntimeError(
            "Anthropic response first content block is not a text block "
            f"(type={block_type})"
        )
    return text
