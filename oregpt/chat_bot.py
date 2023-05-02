from typing import Callable

import openai


def _streaming_stdout(message: str) -> None:
    print(message, end="")


class ChatBot:
    def __init__(self, model: str, streaming_callback_handler: Callable[[str], None] = _streaming_stdout):
        self._streaming_callback_handler = streaming_callback_handler
        # Model list: gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
        # https://platform.openai.com/docs/models/overview
        self._model = model
        # TODO
        # Make system role
        # https://community.openai.com/t/the-system-role-how-it-influences-the-chat-behavior/87353
        # https://learn.microsoft.com/ja-jp/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions#system-role
        # self._log = [{"role": "system", "content": f"You are a chat bot."}]
        self._log = []

    def respond(self, message: str):
        self._log.append({"role": "user", "content": message})
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
            self._streaming_callback_handler(chunked_content)
            content += chunked_content
        self._log.append({"role": "assistant", "content": content})
        return content
