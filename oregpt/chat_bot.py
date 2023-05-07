import json
import pathlib
from datetime import datetime

import openai

from oregpt.stdinout import StdInOut


class ChatBot:
    def __init__(self, model: str, std_in_out: StdInOut):
        self._std_in_out = std_in_out
        # Model list: gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
        # https://platform.openai.com/docs/models/overview
        self._model = model

        self._initialize_log()

    @property
    def log(self) -> list[dict[str, str]]:
        return self._log

    def _initialize_log(self) -> None:
        # TODO
        # Make system role
        # https://community.openai.com/t/the-system-role-how-it-influences-the-chat-behavior/87353
        # https://learn.microsoft.com/ja-jp/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions#system-role
        # self._log = [{"role": "system", "content": f"You are a chat bot."}]
        self._log: list[dict[str, str]] = []

    def respond(self, message: str) -> str:
        self._log.append({"role": "user", "content": message})
        with self._std_in_out.print_assistant_thinking():
            # API Reference: https://platform.openai.com/docs/api-reference/completions/create
            response = openai.ChatCompletion.create(
                model=self._model,
                messages=self._log,
                max_tokens=1024,
                temperature=0,
                stream=True,
            )

        content = ""
        for chunk in response:
            chunked_content = chunk["choices"][0]["delta"].get("content", "")
            self._std_in_out.print_assistant(chunked_content)
            content += chunked_content
        self._std_in_out.print_assistant("\n")
        self._log.append({"role": "assistant", "content": content})
        return content

    def save(self, directory: str) -> str:
        path = pathlib.Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        file_name = str(path / datetime.now().strftime("log_%Y-%m-%d-%H-%M-%S.json"))
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(self._log, file, indent=4, ensure_ascii=False)
        return file_name

    def clear(self) -> None:
        self._initialize_log()
