import sys
from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


class CommandBuilder:
    classes: dict[str, Type["Command"]] = dict({})

    def __init__(self, config: dict[str, Any], bot: ChatBot, std_in_out: StdInOut):
        self._config = config
        self._bot = bot
        self._std_in_out = std_in_out

    def build(self, message: str) -> Optional["Command"]:
        messages = message.split(" ")
        command = messages[0].strip()
        args = messages[1:] if len(messages) >= 2 else [""]
        return (
            class_type(self._config, self._bot, self._std_in_out, args)
            if (class_type := self.__class__.classes.get(command))
            else None
        )


def register(cls: Type["Command"]) -> None:
    for representation in cls.representations:
        CommandBuilder.classes["/" + representation] = cls


class Command(ABC):
    representations: list[str] = []

    def __init__(self, config: dict[str, Any], bot: ChatBot, std_in_out: StdInOut, args: list[str]):
        self._config = config
        self._bot = bot
        self._std_in_out = std_in_out
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
        self._std_in_out.print_system("Clear all conversation history")


@register
class HistoryCommand(Command):
    """Show chat history in json format"""

    representations: list[str] = ["history"]

    def execute(self) -> None:
        self._std_in_out.print_system(str(self._bot.log))


@register
class SaveCommand(Command):
    """Save chat hisotry in json format"""

    representations: list[str] = ["save"]

    def execute(self) -> None:
        file_name = self._bot.save(self._config["log"])
        self._std_in_out.print_system(f"Save all conversation history in {file_name}")


@register
class HelpCommand(Command):
    """Show all commands which you can use in this chat tool"""

    representations: list[str] = ["help"]

    def execute(self) -> None:
        for k, v in CommandBuilder.classes.items():
            self._std_in_out.print_system(f"{k}: {v.__doc__}")
