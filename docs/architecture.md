# Architecture & Design Notes

## Overview

The ShopEasy Customer Service Bot is a single-class Python application that wraps
Anthropic's Claude API to provide intelligent, context-aware customer service.

---

## Core Components

### `CustomerServiceBot` class

| Method | Role |
|--------|------|
| `__init__` | Initialises Anthropic client, stores model name, sets system prompt |
| `_get_system_prompt` | Returns the persona and policy instructions for Claude |
| `classify_intent` | Makes a lightweight API call to label the customer's message |
| `generate_response` | Main method — appends to history, calls API, stores reply |
| `reset_conversation` | Clears history for a new customer session |
| `get_conversation_summary` | Builds a temp message list and requests a handoff summary |

---

## Conversation History Design

Anthropic's API is **stateless** — it has no memory between calls. We simulate
memory by maintaining a `conversation_history` list that grows with each turn:

```
[
  {"role": "user",      "content": "Where is my order?"},
  {"role": "assistant", "content": "I'd be happy to help..."},
  {"role": "user",      "content": "Order #12345"},
  {"role": "assistant", "content": "Let me check..."}
]
```

The full list is sent on every API call so Claude always has full context.

The system prompt is passed as a **separate top-level parameter** (not in the
messages array) — this is Anthropic's convention, unlike OpenAI where it goes
as `{"role": "system", ...}`.

---

## Intent Classification

A separate, minimal API call is made with a tightly-scoped classifier prompt.
Using `max_tokens=20` keeps this fast and cheap — it only needs to return
one of five short labels.

The classification result is displayed as a badge in the CLI and used to route
responses (future versions could use it to load specialised prompts per intent).

---

## Two-Call Pattern

Each user turn triggers two API calls:

1. **Classify** (`max_tokens=20`) — fast, cheap, determines intent
2. **Generate** (`max_tokens=400`) — full response with conversation history

This separation keeps the classifier prompt clean and avoids polluting
the main conversation with routing logic.

---

## Key Design Decisions

- **No system message in history** — Anthropic takes `system=` at the top level
- **Immutable history in summary** — `get_conversation_summary` builds a temp
  list so the actual history is never modified
- **Error isolation** — if `generate_response` fails, the failed user message
  is popped from history so the conversation stays consistent
- **Fallback intent** — any unrecognised classifier output falls back to `general`
  rather than crashing

---

## Possible Extensions

- Load environment variables from `.env` using `python-dotenv`
- Add streaming responses for real-time output
- Persist conversation history to a database for analytics
- Add a web interface with FastAPI + WebSockets
- Route different intents to specialised sub-prompts
