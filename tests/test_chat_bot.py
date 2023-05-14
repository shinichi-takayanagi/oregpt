import contextlib
import json

import pytest
from openai import ChatCompletion

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut

DUMMY_CONTENT = "Yep"


@pytest.fixture
def patched_bot(monkeypatch):
    def _create(*args, **kwargs):
        return [{"choices": [{"delta": {"content": DUMMY_CONTENT}}]}]

    # Set monkey patch to avoid this error: https://github.com/prompt-toolkit/python-prompt-toolkit/issues/406
    def _print(*args, **kwargs):
        pass

    @contextlib.contextmanager
    def _print_as_contextmanager(*args, **kwargs):
        yield

    monkeypatch.setattr(ChatCompletion, "create", _create)
    monkeypatch.setattr(StdInOut, "_print", _print)
    monkeypatch.setattr(StdInOut, "print_assistant_thinking", _print_as_contextmanager)
    return ChatBot("ultra-ai", StdInOut({}, lambda: "Dummy"))


def test_respond(patched_bot):
    answer = patched_bot.respond("Hello, world")
    assert DUMMY_CONTENT == answer


def test_save(tmp_path, patched_bot):
    tmp_path.mkdir(exist_ok=True)
    tmp_file = tmp_path / "test.json"
    what_user_said = "Hello, world"
    patched_bot.respond(what_user_said)
    patched_bot.save(str(tmp_file))
    with tmp_file.open("r") as file:
        assert patched_bot.log == json.load(file)


def test_load(tmp_path, patched_bot):
    tmp_path.mkdir(exist_ok=True)
    tmp_file = tmp_path / "test.json"
    what_user_said = "Hello, world"
    patched_bot.respond(what_user_said)
    patched_bot.save(str(tmp_file))
    bot = ChatBot("THE AI", StdInOut({}, lambda: "Dummy"))
    assert bot.log == [{"role": "system", "content": ChatBot.SYSTEM_CONTENT}]
    bot.load(tmp_file)
    assert bot.log == patched_bot.log


def test_clear(patched_bot):
    what_user_said = "Hello, world"
    patched_bot.respond(what_user_said)
    assert patched_bot.log == [
        {"role": "system", "content": ChatBot.SYSTEM_CONTENT},
        {"role": "user", "content": what_user_said},
        {"role": "assistant", "content": DUMMY_CONTENT},
    ]
    patched_bot.clear()
    assert patched_bot._log == [{"role": "system", "content": ChatBot.SYSTEM_CONTENT}]
