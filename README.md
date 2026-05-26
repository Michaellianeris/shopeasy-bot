# ShopEasy Customer Service Bot 

An AI-powered customer service chatbot for ShopEasy, built with **Anthropic's Claude API**. Features a FastAPI web server, a polished streaming chat UI, REST API endpoints, and intent classification — fully containerised with Docker.

---

## Features

- **Docker & Docker Compose** — one command to build and run everything
- **FastAPI Web Server** — modern, fast backend with auto-generated API docs
- **Streaming Chat UI** — browser interface with typing animations and intent badges
- **Intent Classification** — automatically detects what the customer needs
- **Multi-turn Conversations** — remembers full conversation context
- **5 Intent Categories** — order status, product info, returns, tech support, general
- **Conversation Summary** — generates handoff summaries for human agents
- **Session Reset** — cleanly starts a new customer session
- **CLI Mode** — also runs as a terminal chatbot without Docker
- **Unit Tests** — pytest suite covering all core methods

---

## Project Structure

```
shopeasy-bot/
├── shopeasy_bot/
│   ├── __init__.py          # Package exports
│   └── bot.py               # CustomerServiceBot class
├── templates/
│   └── index.html           # Chat UI served by FastAPI
├── tests/
│   └── test_bot.py          # Unit tests
├── docs/
│   └── architecture.md      # Design decisions and architecture notes
├── app.py                   # FastAPI web server
├── Dockerfile               # Multi-stage Docker image
├── docker-compose.yml       # One-command startup
├── .dockerignore            # Files excluded from Docker image
├── .env.example             # Environment variable template
├── .gitignore               # Files excluded from git
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development/testing dependencies
├── setup.py                 # Package setup
└── README.md                # This file
```

---

## Quickstart — Docker (recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- An Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/shopeasy-bot.git
cd shopeasy-bot
```

### 2. Set up your API key

```bash
cp .env.example .env
```

Edit `.env` and add your key:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Build and run

```bash
docker compose up --build
```

### 4. Open the app

Visit **http://localhost:8000** in your browser 

### Useful Docker commands

```bash
# Run in background
docker compose up --build -d

# View logs
docker compose logs -f

# Stop the container
docker compose down

# Rebuild after code changes
docker compose up --build
```

---

## Quickstart — Local (without Docker)

### 1. Clone and enter the project

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

### 4. Set your API key

```bash
# Mac / Linux
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Windows
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5. Start the server

```bash
uvicorn app:app --reload
```

Open **http://localhost:8000** in your browser.

---

## REST API

| Method | Endpoint   | Description                           |
|--------|------------|---------------------------------------|
| `GET`  | `/`        | Serves the chat UI                    |
| `POST` | `/chat`    | Send a message, get reply + intent    |
| `POST` | `/reset`   | Start a new session                   |
| `GET`  | `/summary` | Get a handoff summary                 |
| `GET`  | `/health`  | Health check                          |
| `GET`  | `/docs`    | Interactive API docs (auto-generated) |

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

---

## CLI Mode

Run the bot directly in your terminal without the web server:

```bash
python -m shopeasy_bot.bot
```

| Command         | Action                   |
|-----------------|--------------------------|
| `quit` / `exit` | End the session          |
| `reset`         | Start a new conversation |
| `summary`       | Print a handoff summary  |

---

## Use as a Python Module

```python
from shopeasy_bot import CustomerServiceBot
import os

bot = CustomerServiceBot(api_key=os.getenv("ANTHROPIC_API_KEY"))

reply  = bot.generate_response("Where is my order #12345?")
intent = bot.classify_intent("I want to return a product")  # → "returns"
summary = bot.get_conversation_summary()
bot.reset_conversation()
```

---

## Intent Categories

| Intent              | Example Phrases                                           |
|---------------------|-----------------------------------------------------------|
| `order_status`      | "Where is my order?", "Track my package #123"            |
| `product_info`      | "Do you have wireless headphones?", "Compare X vs Y"     |
| `returns`           | "How do I return an item?", "What's your refund policy?" |
| `technical_support` | "I can't log in", "Payment isn't going through"          |
| `general`           | "Hi!", "What are your business hours?"                   |

---

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

---

## Environment Variables

| Variable            | Required | Description                                   |
|---------------------|----------|-----------------------------------------------|
| `ANTHROPIC_API_KEY` | Yes      | Your API key from console.anthropic.com       |

---

## Built With

- [Anthropic Claude API](https://docs.anthropic.com) — `claude-sonnet-4-5`
- [FastAPI](https://fastapi.tiangolo.com) — web framework
- [Uvicorn](https://www.uvicorn.org) — ASGI server
- [Docker](https://www.docker.com) — containerisation
- Python 3.11

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Michael Lianeris**

