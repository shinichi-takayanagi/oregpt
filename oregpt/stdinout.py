import copy
from dataclasses import dataclass
from typing import Callable, Optional

from prompt_toolkit import HTML, print_formatted_text, prompt
from prompt_toolkit.formatted_text import AnyFormattedText, FormattedText
from prompt_toolkit.styles import Style


@dataclass
class StdInOut:
    style: Style
    bottom_toolbar: Optional[AnyFormattedText] = None

    def input(self) -> str:
        text = FormattedText([("class:user", "<Me> ")])
        return str(prompt(text, style=self.style, bottom_toolbar=self.bottom_toolbar))

    def _print(self, message: str, type: str, end: str) -> None:
        print_formatted_text(FormattedText([(f"class:{type}", message)]), style=self.style, end=end)

    def print_assistant(self, message: str) -> None:
        self._print(message, "assistant", "")

    def print_assistant_prefix(self) -> None:
        self._print("<AI> ", "assistant", "")

    def print_system(self, message: str) -> None:
        self._print(f"<System> {message}", "system", "\n")
