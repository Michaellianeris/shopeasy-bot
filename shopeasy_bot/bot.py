"""
ShopEasy Customer Service Bot
Built with Anthropic's Claude API (claude-sonnet-4-20250514)
Covers: order status, product info, returns, technical support, general inquiries
"""

import os
from typing import Optional
import anthropic


VALID_INTENTS = ["order_status", "product_info", "returns", "technical_support", "general"]


class CustomerServiceBot:
    """AI-powered customer service chatbot for ShopEasy."""

    # ── Task 1 & 2: __init__ + system prompt ──────────────────────────────────

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5"):
        """Set up the Anthropic client, model, conversation history, and system prompt."""

        # Initialize the Anthropic client
        self.client = anthropic.Anthropic(api_key=api_key)

        # Store the model name
        self.model = model

        # Initialize conversation history (list of {"role": ..., "content": ...} dicts)
        self.conversation_history: list[dict] = []

        # Store the system prompt separately (Anthropic uses it as a top-level param,
        # not as a "system" role message inside the messages array)
        self.system_prompt = self._get_system_prompt()

        print("[CustomerServiceBot initialized]")

    def _get_system_prompt(self) -> str:
        """Design the system prompt that defines bot identity, tone, and capabilities."""
        return """You are Alex, a friendly and efficient customer service agent for ShopEasy,
a leading e-commerce platform. You are professional, empathetic, and concise.

You handle five types of customer inquiries:
1. ORDER_STATUS  — tracking, shipping timelines, delivery updates
2. PRODUCT_INFO  — product availability, specs, comparisons, recommendations
3. RETURNS       — return/refund/exchange policy and procedures
4. TECHNICAL_SUPPORT — login issues, account problems, payment errors, site bugs
5. GENERAL       — greetings, company info, or anything else

Key policies to remember:
- Shipping: standard orders ship in 3–5 business days; express in 1–2 business days.
- Returns: 30-day return window; items must be unused and in original packaging;
  refunds process in 5–7 business days to the original payment method.
- Technical issues: guide users step-by-step. Suggest clearing browser cache,
  resetting passwords, or trying a different browser before escalating.
- Escalation contacts: shipping@shopeasy.com, returns@shopeasy.com, tech@shopeasy.com.

Communication guidelines:
- Keep responses concise (2–3 short paragraphs max).
- Be warm and human — never robotic or scripted-sounding.
- Never invent order numbers, tracking codes, prices, or account details.
- If you genuinely cannot help, offer to escalate to a human agent.
- Always end with a question or offer if the issue may not be fully resolved."""

    # ── Task 3: classify_intent ───────────────────────────────────────────────

    def classify_intent(self, user_message: str) -> str:
        """
        Use Claude to classify the customer message into one of five intents.
        Returns one of: order_status, product_info, returns, technical_support, general
        """
        classify_system = """You are an intent classifier for a customer service chatbot.
Given a customer message, respond with ONLY one of these exact labels — no punctuation,
no explanation, nothing else:

- order_status
- product_info
- returns
- technical_support
- general"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=20,          # Only need a single short label
                system=classify_system,
                messages=[{"role": "user", "content": user_message}],
            )
            raw = response.content[0].text.strip().lower().replace("-", "_")
            # Validate; fall back to "general" if unrecognised
            return raw if raw in VALID_INTENTS else "general"
        except Exception as e:
            print(f"[classify_intent error: {e}]")
            return "general"

    # ── Task 4: generate_response ─────────────────────────────────────────────

    def generate_response(self, user_message: str, intent: Optional[str] = None) -> str:
        """
        Generate a helpful response, maintaining full conversation context.

        Args:
            user_message: The customer's latest message.
            intent: Pre-classified intent; will be auto-detected if not provided.

        Returns:
            The assistant's reply as a plain string.
        """
        # Step 1 — classify intent if not already provided
        if intent is None:
            intent = self.classify_intent(user_message)
            print(f"[Intent detected: {intent}]")

        # Step 2 — add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        try:
            # Step 3 — call the API with full conversation history
            response = self.client.messages.create(
                model=self.model,
                max_tokens=400,
                system=self.system_prompt,
                messages=self.conversation_history,
            )

            # Step 4 — extract assistant text
            assistant_message = response.content[0].text

            # Step 5 — add assistant reply to history for future context
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            return assistant_message

        except Exception as e:
            error_msg = (
                "I apologize, but I'm having trouble processing your request right now. "
                "Please try again in a moment, or contact us directly at support@shopeasy.com."
            )
            print(f"[generate_response error: {e}]")
            # Don't push broken exchange into history
            self.conversation_history.pop()
            return error_msg

    # ── Task 5: reset_conversation ────────────────────────────────────────────

    def reset_conversation(self) -> None:
        """Clear the conversation history so a new customer session can begin."""
        self.conversation_history = []
        print("[Conversation reset]")

    # ── Task 6: get_conversation_summary ──────────────────────────────────────

    def get_conversation_summary(self) -> str:
        """
        Ask Claude to summarise the current conversation for human-agent handoff.
        Does NOT modify conversation_history.
        """
        if not self.conversation_history:
            return "No conversation to summarise yet."

        summary_request = (
            "Please provide a brief handoff summary of this customer service conversation. "
            "Include:\n"
            "1. Main customer concerns or questions\n"
            "2. Information or solutions provided\n"
            "3. Current status and any open next steps\n\n"
            "Keep it to 2–3 concise sentences, written for a human support agent."
        )

        # Build a temporary message list — don't mutate history
        summary_messages = self.conversation_history + [
            {"role": "user", "content": summary_request}
        ]

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=250,
                system=self.system_prompt,
                messages=summary_messages,
            )
            return response.content[0].text
        except Exception as e:
            print(f"[get_conversation_summary error: {e}]")
            return "Unable to generate summary at this time."


# ── Task 7: main chat loop ────────────────────────────────────────────────────

def main() -> None:
    """Interactive CLI chat loop for the ShopEasy customer service bot."""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("Error: Please set the ANTHROPIC_API_KEY environment variable.")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    bot = CustomerServiceBot(api_key)

    print("\n" + "=" * 55)
    print("  ShopEasy Customer Service Bot")
    print("  Type 'quit' to exit | 'reset' for new session")
    print("  Type 'summary' to get a handoff summary")
    print("=" * 55 + "\n")

    # Warm greeting to kick off the conversation
    opening = bot.generate_response(
        "Hi, I just connected to customer service.",
        intent="general",
    )
    print(f"Alex: {opening}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        command = user_input.lower()

        if command in ("quit", "exit"):
            print("\nThank you for using ShopEasy Customer Service. Have a great day!")
            break

        if command == "reset":
            bot.reset_conversation()
            print("Alex: Starting a fresh conversation! How can I help you today?\n")
            continue

        if command == "summary":
            print("\n── Conversation Summary ──────────────────────────────")
            print(bot.get_conversation_summary())
            print("─────────────────────────────────────────────────────\n")
            continue

        response = bot.generate_response(user_input)
        print(f"\nAlex: {response}\n")


# ── Quick smoke-test (runs when executed directly) ────────────────────────────

def run_tests(api_key: str) -> None:
    """Verify intent classification and response generation work correctly."""
    print("\n── Running intent classification tests ──")
    bot = CustomerServiceBot(api_key)

    test_cases = [
        ("Where is my order #12345?",        "order_status"),
        ("Do you have wireless headphones?",  "product_info"),
        ("What's your return policy?",        "returns"),
        ("I can't log into my account",       "technical_support"),
        ("Hi there!",                         "general"),
    ]

    passed = 0
    for message, expected in test_cases:
        detected = bot.classify_intent(message)
        ok = "✓" if detected == expected else "✗"
        print(f"  {ok}  '{message}'")
        print(f"       expected={expected}, got={detected}")
        if detected == expected:
            passed += 1

    print(f"\n  {passed}/{len(test_cases)} tests passed\n")


if __name__ == "__main__":
    import sys

    api_key = os.getenv("ANTHROPIC_API_KEY", "")

    if "--test" in sys.argv and api_key:
        run_tests(api_key)
    else:
        main()
