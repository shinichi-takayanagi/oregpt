# oregpt

A tiny GPT CLI tool.
You can chat with the GPT model developped by OpenAI and save the conversation as json.

![workflow](https://github.com/shinichi-takayanagi/oregpt/actions/workflows/main.yml/badge.svg)
[![license](https://img.shields.io/github/license/shinichi-takayanagi/oregpt.svg)](https://github.com/shinichi-takayanagi/oregpt/blob/master/LICENSE)
[![release](https://img.shields.io/github/release/shinichi-takayanagi/oregpt.svg)](https://github.com/shinichi-takayanagi/oregpt/releases/latest)
[![python-version](https://img.shields.io/pypi/pyversions/oregpt.svg)](https://pypi.org/project/oregpt/)
[![pypi](https://img.shields.io/pypi/v/oregpt?color=%2334D058&label=pypi%20package)](https://pypi.org/project/oregpt)

![oregpt](https://user-images.githubusercontent.com/24406372/236361796-4a38af2b-b7b6-48e3-8ab6-dcba0be1532f.gif)

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

## Configuration
You can specify the place of conversation `log`,
[style (color etc)](https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html)
and
[the model supported in /v1/chat/completions endpoint provided by OpenAI](https://platform.openai.com/docs/models/overview)
in `~/.oregpt/config.yml`
```yaml
❯ cat ~/.oregpt/config.yml
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
