import pytest

from oregpt.chat_bot import ChatBot
from oregpt.command import (
    ClearCommand,
    CommandBuilder,
    ExitCommand,
    HelpCommand,
    HistoryCommand,
    LoadCommand,
    SaveCommand,
)


def test_command_builder(helpers):
    command_builder = CommandBuilder({}, helpers.make_chat_bot("Yahoo"))
    for command_type in [ExitCommand, ClearCommand, HistoryCommand, SaveCommand, LoadCommand, HelpCommand]:
        for representation in command_type.representations:
            assert isinstance(command_builder.build(f"/{representation}"), command_type)


def test_exit_command(patched_bot):
    command = ExitCommand({}, patched_bot, [])
    with pytest.raises(SystemExit):
        command.execute()


def test_clear_command(patched_bot):
    cl = ClearCommand({}, patched_bot, [])
    patched_bot.respond("Hi, bot-san")
    cl.execute()
    assert patched_bot.log == ChatBot.SYSTEM_ROLE
