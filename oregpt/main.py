import os

import openai
import yaml

from typing import Any
from oregpt.chat_bot import ChatBot

blue = "\033[34m"
green = "\033[32m"
bold = "\033[1m"
reset = "\033[0m"


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
    bot = ChatBot(data["openai"]["model"])
    while True:
        print("\n")
        prompt = input(bold + blue + "Me: " + reset).lower()
        print("\n")
        match prompt:
            case "exit" | "quit" | "q":
                break
            case "clear" | "reboot":
                bot.clear()
                print(f"Clear all conversation history")
            case "save":
                file_name = bot.save(data["log"])
                print(f"Save all conversation history in {file_name}")
            case _:
                bot.respond(prompt)


if __name__ == "__main__":
    main()
