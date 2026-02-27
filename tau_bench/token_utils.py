# Copyright Sierra

import json
from typing import List, Dict, Any, Optional

# Default max context length for the deployed model
DEFAULT_MAX_CONTEXT_LENGTH = 4096
# Reserve tokens for the model's response
RESPONSE_TOKEN_RESERVE = 1024


def estimate_token_count(text: str) -> int:
    """Estimate token count using a conservative ratio (1 token ≈ 5 chars for mixed content)."""
    return len(text) // 5 + 1


def estimate_messages_tokens(messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> int:
    """Estimate total tokens for a list of messages and optional tools definition."""
    total = 0
    for msg in messages:
        # role overhead
        total += 4
        content = msg.get("content") or ""
        total += estimate_token_count(str(content))
        # tool_calls in assistant messages
        if "tool_calls" in msg and msg["tool_calls"]:
            total += estimate_token_count(json.dumps(msg["tool_calls"]))
        # function_call
        if "function_call" in msg and msg["function_call"]:
            total += estimate_token_count(json.dumps(msg["function_call"]))
    if tools:
        total += estimate_token_count(json.dumps(tools))
    return total


def truncate_messages(
    messages: List[Dict[str, Any]],
    max_context_length: int = DEFAULT_MAX_CONTEXT_LENGTH,
    response_reserve: int = RESPONSE_TOKEN_RESERVE,
    tools: Optional[List[Dict[str, Any]]] = None,
) -> List[Dict[str, Any]]:
    """Truncate messages to fit within the max context length.

    Strategy:
    - Always keep the system message (first message) and the most recent messages.
    - Remove older conversation messages from the middle when the total exceeds the limit.
    - Also truncates individual message content if a single message is too long.
    """
    if not messages:
        return messages

    token_budget = max_context_length - response_reserve
    tools_tokens = estimate_token_count(json.dumps(tools)) if tools else 0
    available_for_messages = token_budget - tools_tokens

    if available_for_messages <= 0:
        # Even tools alone exceed the budget; just keep the last message
        return messages[-1:]

    # Check if we're already within budget
    current_tokens = estimate_messages_tokens(messages)
    if current_tokens <= available_for_messages:
        return messages

    # Separate system message(s) from conversation messages
    system_messages = []
    conv_messages = []
    for msg in messages:
        if msg.get("role") == "system":
            system_messages.append(msg)
        else:
            conv_messages.append(msg)

    # First, truncate long individual message contents
    def truncate_content(msg: Dict[str, Any], max_chars: int = 3000) -> Dict[str, Any]:
        msg = msg.copy()
        content = msg.get("content")
        if content and isinstance(content, str) and len(content) > max_chars:
            msg["content"] = content[:max_chars] + "\n...[truncated]"
        return msg

    system_messages = [truncate_content(m, max_chars=4000) for m in system_messages]
    conv_messages = [truncate_content(m) for m in conv_messages]

    # Calculate system message tokens
    system_tokens = estimate_messages_tokens(system_messages)

    # Budget remaining for conversation messages
    conv_budget = available_for_messages - system_tokens
    if conv_budget <= 0:
        # System message alone exceeds the budget; truncate it further
        if system_messages:
            sys_msg = system_messages[0].copy()
            max_sys_chars = available_for_messages * 3  # rough inverse of estimate
            content = sys_msg.get("content", "")
            if len(content) > max_sys_chars:
                sys_msg["content"] = content[:max_sys_chars] + "\n...[truncated]"
            return [sys_msg] + conv_messages[-1:]
        return conv_messages[-1:]

    # Keep removing oldest conversation messages until we fit
    # Always try to keep the first user message and the most recent messages
    while len(conv_messages) > 1:
        current_conv_tokens = estimate_messages_tokens(conv_messages)
        if current_conv_tokens <= conv_budget:
            break
        # Remove the oldest conversation message (index 0), but try to keep at least the last 2
        if len(conv_messages) <= 2:
            # Truncate the remaining messages more aggressively
            conv_messages = [truncate_content(m, max_chars=500) for m in conv_messages]
            break
        conv_messages.pop(0)

    result = system_messages + conv_messages

    # Final safety check: if still too long, aggressively truncate all content
    if estimate_messages_tokens(result) > available_for_messages:
        result = [truncate_content(m, max_chars=300) for m in result]

    return result
