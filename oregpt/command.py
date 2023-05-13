from typing import Any
import sys
from abc import ABC, abstractmethod

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


class CommandBuilder:
    classes = dict({})

    def __init__(self, config: dict[str, Any], bot: ChatBot, std_in_out: StdInOut):
        self._config = config
        self._bot = bot
        self._std_in_out = std_in_out

    def build(self, command: str):
        return (
            class_type(self._config, self._bot, self._std_in_out)
            if (class_type := self.__class__.classes.get(command))
            else None
        )


def register(cls):
    for representation in cls.representations:
        CommandBuilder.classes[representation] = cls
    return cls


class Command(ABC):
    def __init__(self, bot: ChatBot, std_in_out: StdInOut):
        self._bot = bot
        self._std_in_out = std_in_out

    @abstractmethod
    def execute(self) -> None:
        pass


@register
class ExitCommand(Command):
    representations: list[str] = ["exit", "quit", "q"]

    def execute(self) -> None:
        sys.exit()


@register
class ClearCommand(Command):
    representations: list[str] = ["clear"]

    def execute(self) -> None:
        self._bot.clear()
        self._std_in_out.print_system("Clear all conversation history")


@register
class HistoryCommand(Command):
    representations: list[str] = ["history"]

    def execute(self) -> None:
        self._std_in_out.print_system(str(self._bot.log))


@register
class SaveCommand(Command):
    representations: list[str] = ["save"]

    def execute(self) -> None:
        file_name = self._bot.save(self._config["log"])
        self._std_in_out.print_system(f"Save all conversation history in {file_name}")
