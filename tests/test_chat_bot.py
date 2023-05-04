from openai import ChatCompletion
from prompt_toolkit.styles import Style

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


def test_chat_bot_respond(monkeypatch):
    # Patch for openai.ChatCompletion.create
    def create(*args, **kwargs):
        return [{"choices": [{"delta": {"content": "Yep"}}]}]

    monkeypatch.setattr(ChatCompletion, "create", create)

    bot = ChatBot("hoge", StdInOut(Style.from_dict({}), None))
    answer = bot.respond("Hello, world")
    assert "Yep" == answer
