import os
import pathlib
import shutil
from typing import Any

import openai
import yaml

from oregpt.chat_bot import ChatBot
from oregpt.stdinout import StdInOut


def load_config() -> dict[str, Any]:
    # TODO: Find more sophisticated way to do this...
    config_file = os.path.join(os.path.expanduser("~"), ".config/oregpt/config.yml")
    if not os.path.exists(config_file):
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        directory = pathlib.Path(__file__).parent.resolve()
        shutil.copyfile(directory / "resources/config.yml", config_file)
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


def main() -> int:
    config = load_config()
    initialize_open_ai_key(config["openai"])
    std_in_out = StdInOut(config["character"], lambda: "To exit, type q, quit, exit, or Ctrl + C")
    bot = ChatBot(config["openai"]["model"], std_in_out)

    try:
        while True:
            message = std_in_out.input().lower()
            match message:
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
                    bot.respond(message)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        raise Exception(f"Something happened: {str(e)}") from e
    return 0


if __name__ == "__main__":
    main()
