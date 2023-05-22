import os
import pathlib
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional, Type

from oregpt.chat_bot import ChatBot


class CommandBuilder:
    command_classes: dict[str, Type["Command"]] = dict({})

    def __init__(self, config: dict[str, Any], bot: ChatBot):
        self._config = config
        self._bot = bot

    def build(self, message: str) -> Optional["Command"]:
        messages = message.split(" ")
        command = messages[0].strip()
        args = messages[1:] if len(messages) >= 2 else []
        args = list(filter(None, args))
        return (
            class_type(self._config, self._bot, args)
            if (class_type := CommandBuilder.command_classes.get(command))
            else None
        )

    def looks_like_command(self, message: str) -> bool:
        if len(message) == 0:
            return False
        return "/" == message[0]


def register(cls: Type["Command"]) -> Type["Command"]:
    for representation in cls.representations:
        CommandBuilder.command_classes["/" + representation] = cls
    return cls


class Command(ABC):
    representations: list[str] = []

    def __init__(self, config: dict[str, Any], bot: ChatBot, args: list[str]):
        self._config = config
        self._bot = bot
        self._args = args

    @abstractmethod
    def execute(self) -> None:
        pass


@register
class ExitCommand(Command):
    """Exit from this chat tool"""

    representations: list[str] = ["exit", "quit", "q"]

    def execute(self) -> None:
        sys.exit()


@register
class ClearCommand(Command):
    """Clear chat history all"""

    representations: list[str] = ["clear"]

    def execute(self) -> None:
        self._bot.clear()
        self._bot.std_in_out.print_system("Clear all conversation history")


@register
class HistoryCommand(Command):
    """Show chat history in json format"""

    representations: list[str] = ["history"]

    def execute(self) -> None:
        self._bot.std_in_out.print_system(str(self._bot.log))


def _abspath(x: str) -> str:
    return os.path.abspath(os.path.expanduser(x))


@register
class SaveCommand(Command):
    """Save chat history in json format"""

    representations: list[str] = ["save"]

    def execute(self) -> None:
        file_name = ""
        if len(self._args) == 1:
            file_name = _abspath(self._args[0].strip())
            directory = pathlib.Path(os.path.dirname(file_name))
        if file_name == "":
            directory = pathlib.Path(_abspath(self._config["log"]))
            file_name = str(directory / datetime.now().strftime("log_%Y-%m-%d-%H-%M-%S.json"))
        directory.mkdir(parents=True, exist_ok=True)
        self._bot.save(file_name)
        self._bot.std_in_out.print_system(f"Save all conversation history in {file_name}")


@register
class LoadCommand(Command):
    """Load chat history from a json file"""

    representations: list[str] = ["load"]

    def execute(self) -> None:
        print(self._args)
        if len(self._args) != 1:
            self._bot.std_in_out.print_system("Loaded file was not specified as an argument")
            return
        file_name = _abspath(self._args[0])
        self._bot.load(file_name)
        self._bot.std_in_out.print_system(f"Loaded chat history from {file_name}")


@register
class HelpCommand(Command):
    """Show all commands which you can use in this chat tool"""

    representations: list[str] = ["help"]

    def execute(self) -> None:
        for k, v in CommandBuilder.command_classes.items():
            self._bot.std_in_out.print_system(f"{k}: {v.__doc__}")
