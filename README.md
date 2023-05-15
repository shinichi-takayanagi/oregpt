# oregpt
![workflow](https://github.com/shinichi-takayanagi/oregpt/actions/workflows/main.yml/badge.svg)
[![license](https://img.shields.io/github/license/shinichi-takayanagi/oregpt.svg)](https://github.com/shinichi-takayanagi/oregpt/blob/master/LICENSE)
[![release](https://img.shields.io/github/release/shinichi-takayanagi/oregpt.svg)](https://github.com/shinichi-takayanagi/oregpt/releases/latest)
[![python-version](https://img.shields.io/pypi/pyversions/oregpt.svg)](https://pypi.org/project/oregpt/)
[![pypi](https://img.shields.io/pypi/v/oregpt?color=%2334D058&label=pypi%20package)](https://pypi.org/project/oregpt)

A tiny GPT CLI tool.
You can chat with the GPT model developped by OpenAI and save the conversation as json.

<img src="https://github.com/shinichi-takayanagi/oregpt/assets/24406372/91969861-9f29-4c81-9505-620ef5567a5b" width="800px">

## Installation
### Get your own OpenAI API Key
Assuming you have an environment variable with key named `OPENAI_API_KEY`.
If you don't have a OpenAI API key [visit here](https://platform.openai.com/account/api-keys), generate one and add it as an environment variable

```bash
export OPENAI_API_KEY=<YOUR-OPENAI-API-KEY>

```

### Instal from PyPI
You can install the package using pip:

```bash
$ pip install oregpt
```

## Usage
Once you have installed oregpt, you can run it by typing:
```bash
$ oregpt
```

## Supported commands on chat
Commands such as saving and loading conversations are available as the following:

|  Command  |  Description  |
| ---- | ---- |
| `/exit`    | Exit from this chat tool |
| `/quit`    | Exit from this chat tool |
| `/q`       | Exit from this chat tool |
| `/clear`   | Clear chat history all |
| `/history` | Show chat history in json format |
| `/save`    | Save chat hisotry in json format |
| `/load`    | Load chat hisotry from a json file |
| `/help`    | Show all commands which you can use in this chat tool |

## Configuration
You can specify the place of conversation `log`,
[style (color etc)](https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html)
and
[the model supported in /v1/chat/completions endpoint provided by OpenAI](https://platform.openai.com/docs/models/overview)
in `~/.config/oregpt/config.yml`
```yaml
❯ cat ~/.config/oregpt/config.yml
log: /tmp/oregpt/
openai:
    model: gpt-3.5-turbo
# You can also specify OpenAI's API key here
#     api_key: <your-api-key>
character:
    user:
        name: Me
        style: "#00BEFE"
    assistant:
        name: AI
        style: "#87CEEB"
    system:
        name: System
        style: "#cc0000"
```
