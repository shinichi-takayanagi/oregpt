import os
import pathlib
import shutil
from enum import Enum
from typing import Any, Optional

import click
import openai
import yaml

from oregpt.chat_bot import ChatBot
from oregpt.command import CommandBuilder
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


class Status(Enum):
    USER = 1
    BOT = 2


def prefer_left(lhs: str, rhs: Optional[str]) -> str:
    if lhs != "":
        return lhs
    if rhs is not None:
        return rhs
    raise Exception("Set as an argument or in ~/.config/oregpt/config.yml")


# Add "type: ignore" to avoid this https://github.com/python/typeshed/issues/6156
@click.command()  # type: ignore
@click.option("--model_name", "-m", type=str, help="Model name in OpenAI (e.g, gpt-3.5-turbo, gpt-4)", default="")  # type: ignore
@click.option("--assistant_role", "-a", type=str, help="Role setting for Assistant (AI)", default="")  # type: ignore
def main(model_name: str, assistant_role: str) -> int:
    config = load_config()
    initialize_open_ai_key(config["openai"])
    model_name = prefer_left(model_name, config["openai"].get("model"))
    assistant_role = prefer_left(assistant_role, config["character"]["assistant"].get("role"))
    std_in_out = StdInOut(config["character"], lambda: "To exit, type /q, /quit, /exit, or Ctrl + C")
    bot = ChatBot(model_name, assistant_role, std_in_out)
    command_builder = CommandBuilder(config, bot)

    while True:
        try:
            status = Status.USER
            message = std_in_out.input().lower()
            if command := command_builder.build(message):
                command.execute()
            else:
                status = Status.BOT
                if command_builder.looks_like_command(message):
                    std_in_out.print_system("Invalid command. Valid commands are as the following:")
                    command_builder.build("/help").execute()  # type: ignore
                else:
                    bot.respond(message)
        except KeyboardInterrupt:
            if status == Status.BOT:
                std_in_out.print_assistant("\n")
            else:
                return 0
        except Exception as e:
            raise Exception(f"Something happened: {str(e)}") from e
            return 1

    return 0


if __name__ == "__main__":
    main()
