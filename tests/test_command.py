import pytest

from oregpt.command import (
    ClearCommand,
    CommandBuilder,
    ExitCommand,
    HelpCommand,
    HistoryCommand,
    LoadCommand,
    SaveCommand,
)


def test_command_builder_build(helpers):
    command_builder = CommandBuilder({}, helpers.make_chat_bot("Yahoo", "You are a bot"))
    for command_type in [ExitCommand, ClearCommand, HistoryCommand, SaveCommand, LoadCommand, HelpCommand]:
        for representation in command_type.representations:
            assert isinstance(command_builder.build(f"/{representation}"), command_type)


def test_command_builder_looks_like_command(helpers):
    command_builder = CommandBuilder({}, helpers.make_chat_bot("Yahoo", "You are a bot"))
    assert command_builder.looks_like_command("/hoge hoge") == True
    assert command_builder.looks_like_command("/hoge") == True
    assert command_builder.looks_like_command("/") == True
    assert command_builder.looks_like_command("hoge hoge") == False
    assert command_builder.looks_like_command("hoge") == False
    assert command_builder.looks_like_command("") == False


def test_exit_command(patched_bot):
    command = ExitCommand({}, patched_bot, [])
    with pytest.raises(SystemExit):
        command.execute()


def test_clear_command(patched_bot):
    cl = ClearCommand({}, patched_bot, [])
    patched_bot.respond("Hi, bot-san")
    cl.execute()
    assert patched_bot.log == patched_bot.assistant_role
