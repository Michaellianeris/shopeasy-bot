"""
Unit tests for CustomerServiceBot.
Run with: pytest tests/ -v
"""

import pytest
from unittest.mock import MagicMock, patch
from shopeasy_bot.bot import CustomerServiceBot, VALID_INTENTS


@pytest.fixture
def bot():
    """Create a bot instance with a fake API key for testing."""
    with patch("anthropic.Anthropic"):
        return CustomerServiceBot(api_key="sk-ant-test-key")


class TestInit:
    def test_model_default(self, bot):
        assert bot.model == "claude-sonnet-4-5"

    def test_history_starts_empty(self, bot):
        assert bot.conversation_history == []

    def test_system_prompt_set(self, bot):
        assert "ShopEasy" in bot.system_prompt
        assert "Alex" in bot.system_prompt


class TestClassifyIntent:
    @pytest.mark.parametrize("message,expected", [
        ("Where is my order #123?",        "order_status"),
        ("Do you have wireless headphones?","product_info"),
        ("What is your return policy?",     "returns"),
        ("I can't log into my account",     "technical_support"),
        ("Hi there!",                       "general"),
    ])
    def test_intent_classification(self, bot, message, expected):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=expected)]
        bot.client.messages.create.return_value = mock_response

        result = bot.classify_intent(message)
        assert result == expected

    def test_invalid_intent_falls_back_to_general(self, bot):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="unknown_intent")]
        bot.client.messages.create.return_value = mock_response

        result = bot.classify_intent("some message")
        assert result == "general"

    def test_api_error_falls_back_to_general(self, bot):
        bot.client.messages.create.side_effect = Exception("API error")
        result = bot.classify_intent("some message")
        assert result == "general"


class TestGenerateResponse:
    def test_adds_to_history(self, bot):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello! How can I help?")]
        bot.client.messages.create.return_value = mock_response

        bot.generate_response("Hi", intent="general")

        assert len(bot.conversation_history) == 2
        assert bot.conversation_history[0]["role"] == "user"
        assert bot.conversation_history[1]["role"] == "assistant"

    def test_returns_string(self, bot):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Here is my reply.")]
        bot.client.messages.create.return_value = mock_response

        result = bot.generate_response("Hello", intent="general")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_error_returns_fallback_message(self, bot):
        bot.client.messages.create.side_effect = Exception("API down")
        result = bot.generate_response("Hello", intent="general")
        assert "trouble" in result.lower()


class TestReset:
    def test_clears_history(self, bot):
        bot.conversation_history = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello"},
        ]
        bot.reset_conversation()
        assert bot.conversation_history == []

    def test_reset_multiple_times(self, bot):
        for _ in range(3):
            bot.reset_conversation()
        assert bot.conversation_history == []


class TestSummary:
    def test_no_history_returns_message(self, bot):
        result = bot.get_conversation_summary()
        assert "no conversation" in result.lower()

    def test_summary_with_history(self, bot):
        bot.conversation_history = [
            {"role": "user", "content": "Where is my order?"},
            {"role": "assistant", "content": "I can help with that!"},
        ]
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Customer asked about order status.")]
        bot.client.messages.create.return_value = mock_response

        result = bot.get_conversation_summary()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_summary_does_not_modify_history(self, bot):
        bot.conversation_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"},
        ]
        original_len = len(bot.conversation_history)
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Summary here.")]
        bot.client.messages.create.return_value = mock_response

        bot.get_conversation_summary()
        assert len(bot.conversation_history) == original_len
