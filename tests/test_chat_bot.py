from openai import ChatCompletion

from oregpt.chat_bot import ChatBot


def test_chat_bot_respond(monkeypatch):
    # Patch for openai.ChatCompletion.create
    def create(*args, **kwargs):
        return [{"choices": [{"delta": {"content": "Yep"}}]}]

    monkeypatch.setattr(ChatCompletion, "create", create)

    bot = ChatBot("hoge")
    answer = bot.respond("Hello, world")
    assert "Yep" == answer
