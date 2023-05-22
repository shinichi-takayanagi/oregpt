import json

import pytest


@pytest.fixture
def tmp_file(tmpdir_factory):
    return tmpdir_factory.mktemp("data").join("test.json")


def test_initialized_property(helpers):
    bot = helpers.make_chat_bot("THE AI", "You are a bot")
    assert bot.model == "THE AI"
    assert bot.log == bot.assistant_role


def test_respond_and_log(patched_bot):
    what_user_said = "Hello, world"
    assert patched_bot.log == patched_bot.assistant_role
    assert pytest.DUMMY_CONTENT == patched_bot.respond(what_user_said)
    assert patched_bot.log == patched_bot.assistant_role + [
        {"role": "user", "content": what_user_said},
        {"role": "assistant", "content": pytest.DUMMY_CONTENT},
    ]


def test_save(tmp_file, patched_bot):
    what_user_said = "Hello, world???"
    patched_bot.respond(what_user_said)
    patched_bot.save(str(tmp_file))

    with tmp_file.open("r") as file:
        assert patched_bot.log == json.load(file)
        assert patched_bot.log == patched_bot.assistant_role + [
            {"role": "user", "content": what_user_said},
            {"role": "assistant", "content": pytest.DUMMY_CONTENT},
        ]


def test_load(tmp_file, patched_bot, helpers):
    what_user_said = "Hello, world"
    patched_bot.respond(what_user_said)
    patched_bot.save(str(tmp_file))

    bot = helpers.make_chat_bot("THE AI", "You are a bot")
    bot.load(tmp_file)
    assert bot.log == patched_bot.log


def test_clear(patched_bot):
    what_user_said = "Hello, world"
    patched_bot.respond(what_user_said)
    assert patched_bot.log == patched_bot.assistant_role + [
        {"role": "user", "content": what_user_said},
        {"role": "assistant", "content": pytest.DUMMY_CONTENT},
    ]
    patched_bot.clear()
    assert patched_bot._log == patched_bot.assistant_role
