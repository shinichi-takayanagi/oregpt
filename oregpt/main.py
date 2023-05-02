import os

import openai
import yaml

from oregpt.chat_bot import ChatBot

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("config.yml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

blue = "\033[34m"
green = "\033[32m"
bold = "\033[1m"
reset = "\033[0m"


def main():
    bot = ChatBot(data["model"])
    while True:
        print("")
        prompt = input(bold + blue + "Enter a prompt: " + reset)
        if prompt.lower() in ["q", "exit", "quit"]:
            break
        bot.respond(prompt)


if __name__ == "__main__":
    main()
