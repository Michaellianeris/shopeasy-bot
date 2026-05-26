# ShopEasy Customer Service Bot 🛒

An AI-powered customer service chatbot for ShopEasy, built with **Anthropic's Claude API**. Handles order tracking, product inquiries, returns, technical support, and general questions — with full multi-turn conversation memory.

---

## Features

- **Intent Classification** — automatically detects what the customer needs
- **Multi-turn Conversations** — remembers full conversation context
- **5 Intent Categories** — order status, product info, returns, tech support, general
- **Conversation Summary** — generates handoff summaries for human agents
- **Session Reset** — cleanly starts a new customer session
- **Error Handling** — graceful fallbacks on API failures

---

## Project Structure

```
shopeasy-bot/
├── shopeasy_bot/
│   ├── __init__.py        # Package exports
│   └── bot.py             # Main CustomerServiceBot class
├── tests/
│   └── test_bot.py        # Unit tests
├── docs/
│   └── architecture.md    # Design decisions and architecture notes
├── .env.example           # Environment variable template
├── .gitignore             # Files to exclude from git
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
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Copy the example env file and add your key:

```bash
cp .env.example .env
```

Edit `.env`:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Or export it directly in your terminal:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### 5. Run the bot

```bash
python -m shopeasy_bot.bot
```

---

## Usage

### CLI Chat Mode

```bash
python -m shopeasy_bot.bot
```

Available commands during chat:

| Command | Action |
|---------|--------|
| `quit` / `exit` | End the session |
| `reset` | Start a new conversation |
| `summary` | Print a handoff summary |

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

| Intent | Example Phrases |
|--------|----------------|
| `order_status` | "Where is my order?", "Track my package #123" |
| `product_info` | "Do you have wireless headphones?", "What's the difference between X and Y?" |
| `returns` | "How do I return an item?", "What's your refund policy?" |
| `technical_support` | "I can't log in", "Payment isn't going through" |
| `general` | "Hi!", "What are your business hours?" |

---

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key from console.anthropic.com |

---

## Built With

- [Anthropic Claude API](https://docs.anthropic.com) — `claude-sonnet-4-5`
- Python 3.9+

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Michael Lianeris**  
Built as part of the Udacity AI course — Implementing a Chatbot with an LLM.
