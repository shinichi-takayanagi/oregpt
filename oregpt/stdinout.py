import contextlib
import sys
from dataclasses import dataclass
from typing import Any, Iterator, Optional

from prompt_toolkit import print_formatted_text, prompt
from prompt_toolkit.formatted_text import AnyFormattedText, FormattedText
from prompt_toolkit.styles import Style


@dataclass
class Character:
    name: str
    style: str


class StdInOut:
    def __init__(self, config: dict[str, Any], bottom_toolbar: Optional[AnyFormattedText]):
        self._characters: dict[str, Character] = {}
        for key, value in config.items():
            self._characters[key] = Character(**value)
        self._bottom_toolbar = bottom_toolbar

    def input(self) -> str:
        text = FormattedText([("class:user", f"<{self._characters['user'].name}> ")])
        return str(prompt(text, style=self._style(), bottom_toolbar=self._bottom_toolbar))

    def _style(self) -> Style:
        return Style.from_dict(
            {
                "": self._characters["user"].style,
                "user": self._characters["user"].style,
                "assistant": self._characters["assistant"].style,
                "assistant-blink": self._characters["assistant"].style + " blink",
                "system": self._characters["system"].style,
            }
        )

    def _print(self, message_decorated: list[tuple[str, str]], end: str) -> None:
        print_formatted_text(FormattedText(message_decorated), style=self._style(), end=end)

    def print_assistant(self, message: str) -> None:
        self._print([("class:assistant", message)], "")

    @contextlib.contextmanager
    def print_assistant_thinking(self) -> Iterator[None]:
        name = self._characters["assistant"].name
        message_decorated = [("class:assistant", f"<{name}> "), ("class:assistant-blink", "I'm thinking...")]
        self._print(message_decorated, "")
        yield
        # Clear the above message (I'm thinking...)
        sys.stdout.write("\033[2K\033[G")
        sys.stdout.flush()
        self._print([("class:assistant", f"<{name}> ")], "")

    def print_system(self, message: str) -> None:
        self._print([("class:system", f"<{self._characters['system'].name}> {message}")], "\n")
