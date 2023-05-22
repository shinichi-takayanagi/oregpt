import contextlib

import pytest
from openai import ChatCompletion

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


def pytest_configure():
    # https://stackoverflow.com/questions/44441929/how-to-share-global-variables-between-tests
    pytest.DUMMY_CONTENT = "Yep"


# Use this trick
# https://stackoverflow.com/a/42156088/3926333
class Helpers:
    @staticmethod
    def make_std_in_out():
        return StdInOut({}, lambda: "Dummy")

    @staticmethod
    def make_chat_bot(name: str, role: str):
        return ChatBot(name, role, Helpers.make_std_in_out())


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture
def patched_bot(monkeypatch, helpers):
    def _create(*args, **kwargs):
        return [{"choices": [{"delta": {"content": pytest.DUMMY_CONTENT}}]}]

    # Set monkey patch to avoid this error: https://github.com/prompt-toolkit/python-prompt-toolkit/issues/406
    def _print(*args, **kwargs):
        pass

    @contextlib.contextmanager
    def _print_as_contextmanager(*args, **kwargs):
        yield

    monkeypatch.setattr(ChatCompletion, "create", _create)
    monkeypatch.setattr(StdInOut, "_print", _print)
    monkeypatch.setattr(StdInOut, "print_assistant_thinking", _print_as_contextmanager)
    return helpers.make_chat_bot("THE AI", "You are a great chat bot")
