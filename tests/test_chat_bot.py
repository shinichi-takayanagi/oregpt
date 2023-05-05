from openai import ChatCompletion
from prompt_toolkit.styles import Style

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


def test_chat_bot_respond(monkeypatch):
    def _create(*args, **kwargs):
        return [{"choices": [{"delta": {"content": "Yep"}}]}]

    def _print(*args, **kwargs):
        pass

    monkeypatch.setattr(ChatCompletion, "create", _create)
    monkeypatch.setattr(StdInOut, "_print", _print)

    bot = ChatBot("hoge", StdInOut(Style.from_dict({}), None))
    answer = bot.respond("Hello, world")
    assert "Yep" == answer
