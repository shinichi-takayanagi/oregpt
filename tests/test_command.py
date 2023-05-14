from oregpt.command import CommandBuilder, ExitCommand


def test_command_builder(helpers):
    command_builder = CommandBuilder({}, helpers.make_chat_bot("Yahoo"))
    assert isinstance(command_builder.build("/q"), ExitCommand)
