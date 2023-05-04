import os
from typing import Any

import openai
import yaml
from prompt_toolkit.styles import Style

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


def initialize_open_ai_key(data: dict[str, Any]) -> None:
    if "api_key" in data["openai"]:
        openai.api_key = data["openai"]["api_key"]
        return
    if value := os.getenv("OPENAI_API_KEY"):
        openai.api_key = value
        return

    raise LookupError("OpenAI's API key was not found in config.yml and environment variables")


def main() -> None:
    with open("config.yml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    initialize_open_ai_key(data)
    std_in_out = StdInOut(
        Style.from_dict(
            {"": data["style"]["user"], "assistant": data["style"]["assistant"], "system": data["style"]["system"]}
        ),
        lambda: "To exit, type q, quit or exit",
    )
    bot = ChatBot(data["openai"]["model"], std_in_out)

    while True:
        text = std_in_out.input().lower()
        match text:
            case "exit" | "quit" | "q":
                break
            case "clear":
                bot.clear()
                std_in_out.print_system("Clear all conversation history")
            case "history":
                std_in_out.print_system(str(bot.log))
            case "save":
                file_name = bot.save(data["log"])
                std_in_out.print_system(f"Save all conversation history in {file_name}")
            case _:
                bot.respond(text)


if __name__ == "__main__":
    main()
