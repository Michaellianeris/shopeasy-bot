# ShopEasy Customer Service Bot 

An AI-powered customer service chatbot for ShopEasy, built with **Anthropic's Claude API**. Includes a FastAPI web server, a polished chat UI, REST API endpoints, intent classification, and full multi-turn conversation memory.

---

## Features

- **FastAPI Web Server** — modern, fast backend with auto-generated API docs
- **Chat UI** — clean browser-based interface with streaming responses and typing animations
- **Intent Classification** — automatically detects what the customer needs
- **Multi-turn Conversations** — remembers full conversation context
- **5 Intent Categories** — order status, product info, returns, tech support, general
- **Conversation Summary** — generates handoff summaries for human agents
- **Session Reset** — cleanly starts a new customer session
- **CLI Mode** — also runs as a terminal chatbot without the web server
- **Unit Tests** — pytest test suite covering all core methods

---

## Project Structure

```
shopeasy-bot/
├── shopeasy_bot/
│   ├── __init__.py        # Package exports
│   └── bot.py             # CustomerServiceBot class
├── templates/
│   └── index.html         # Chat UI served by FastAPI
├── tests/
│   └── test_bot.py        # Unit tests
├── docs/
│   └── architecture.md    # Design decisions and architecture notes
├── app.py                 # FastAPI web server
├── .env.example           # Environment variable template
├── .gitignore             # Files excluded from git
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development/testing dependencies
├── setup.py               # Package setup
└── README.md              # This file
```

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/shopeasy-bot.git
cd shopeasy-bot
```

### 2. Create and activate a virtual environment

```bash
# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and fill in your key:

```bash
cp .env.example .env
```

Edit `.env`:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Or export it directly in your terminal:
```bash
# Mac / Linux
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Windows
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5. Start the web server

```bash
uvicorn app:app --reload
```

Then open your browser at **http://localhost:8000** 

---

## Usage

### Web UI (recommended)

Start the server and open http://localhost:8000 in your browser. The chat interface supports:
- Live streaming responses with typing animation
- Intent badge shown on every reply
- Quick suggestion buttons
- Conversation summary panel
- Session reset

### REST API

| Method | Endpoint  | Description                          |
|--------|-----------|--------------------------------------|
| `GET`  | `/`       | Serves the chat UI                   |
| `POST` | `/chat`   | Send a message, get reply + intent   |
| `POST` | `/reset`  | Start a new session                  |
| `GET`  | `/summary`| Get a handoff summary                |
| `GET`  | `/health` | Check server status                  |
| `GET`  | `/docs`   | Interactive API docs (auto-generated)|

Example request:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Where is my order #12345?"}'
```

Example response:
```json
{
  "reply": "I'd be happy to help track order #12345...",
  "intent": "order_status"
}
```

### CLI Mode

Run without the web server directly in your terminal:

```bash
python -m shopeasy_bot.bot
```

Available commands during chat:

| Command         | Action                    |
|-----------------|---------------------------|
| `quit` / `exit` | End the session           |
| `reset`         | Start a new conversation  |
| `summary`       | Print a handoff summary   |

### Use as a Python Module

```python
from shopeasy_bot import CustomerServiceBot
import os

bot = CustomerServiceBot(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Generate a response (intent auto-detected)
reply = bot.generate_response("Where is my order #12345?")
print(reply)

# Classify intent only
intent = bot.classify_intent("I want to return a product")
print(intent)  # → "returns"

# Get a conversation summary
summary = bot.get_conversation_summary()

# Reset for a new customer
bot.reset_conversation()
```

---

## Intent Categories

| Intent              | Example Phrases                                          |
|---------------------|----------------------------------------------------------|
| `order_status`      | "Where is my order?", "Track my package #123"           |
| `product_info`      | "Do you have wireless headphones?", "Compare X vs Y"    |
| `returns`           | "How do I return an item?", "What's your refund policy?"|
| `technical_support` | "I can't log in", "Payment isn't going through"         |
| `general`           | "Hi!", "What are your business hours?"                  |

---

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

---

## Environment Variables

| Variable            | Required | Description                                        |
|---------------------|----------|----------------------------------------------------|
| `ANTHROPIC_API_KEY` | Yes      | Your API key from console.anthropic.com            |

---

## Built With

- [Anthropic Claude API](https://docs.anthropic.com) — `claude-sonnet-4-5`
- [FastAPI](https://fastapi.tiangolo.com) — web framework
- [Uvicorn](https://www.uvicorn.org) — ASGI server
- Python 3.9+

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Michael Lianeris**  

