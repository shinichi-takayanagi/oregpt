import contextlib

from openai import ChatCompletion

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


def test_chat_bot_respond(monkeypatch):
    def _create(*args, **kwargs):
        return [{"choices": [{"delta": {"content": "Yep"}}]}]

    # Set monkey patch to avoid this error: https://github.com/prompt-toolkit/python-prompt-toolkit/issues/406
    def _print(*args, **kwargs):
        pass

    @contextlib.contextmanager
    def _print_as_contextmanager(*args, **kwargs):
        yield

    monkeypatch.setattr(ChatCompletion, "create", _create)
    monkeypatch.setattr(StdInOut, "_print", _print)
    monkeypatch.setattr(StdInOut, "print_assistant_thinking", _print_as_contextmanager)

    bot = ChatBot("ultra-ai", StdInOut({}, lambda: "Dummy"))

    answer = bot.respond("Hello, world")
    assert "Yep" == answer
