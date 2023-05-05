import os
import shutil
from typing import Any

import openai
import yaml
from prompt_toolkit.styles import Style

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


def load_config() -> dict[str, Any]:
    # TODO: Find more sophisticated way to do this...
    config_file = os.path.join(os.path.expanduser("~"), ".oregpt/config.yml")
    if not os.path.exists(config_file):
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        shutil.copyfile("config.yml", config_file)
    with open(config_file, "r") as file:
        config: dict[str, Any] = yaml.load(file, Loader=yaml.FullLoader)
    return config


def initialize_open_ai_key(config: dict[str, Any]) -> None:
    if "api_key" in config:
        openai.api_key = config["api_key"]
        return
    if value := os.getenv("OPENAI_API_KEY"):
        openai.api_key = value
        return

    raise LookupError("OpenAI's API key was not found in config.yml and environment variables")


def make_std_in_out(config: dict[str, Any]) -> StdInOut:
    return StdInOut(
        Style.from_dict(
            {
                "": config["user"],  # Default color which is used for "input" should be the same with user
                "user": config["user"],
                "assistant": config["assistant"],
                "system": config["system"],
            }
        ),
        lambda: "To exit, type q, quit or exit",
    )


def main() -> None:
    config = load_config()
    initialize_open_ai_key(config["openai"])
    std_in_out = make_std_in_out(config["style"])
    bot = ChatBot(config["openai"]["model"], std_in_out)

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
                file_name = bot.save(config["log"])
                std_in_out.print_system(f"Save all conversation history in {file_name}")
            case _:
                bot.respond(text)


if __name__ == "__main__":
    main()
