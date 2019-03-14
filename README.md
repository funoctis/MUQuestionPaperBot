# MUQuestionPaperBot
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-green.svg)](https://t.me/MUQuestionPaperBot)

This is a Telegram chatbot that fetches PDFs of questions papers that have been asked by the Mumbai University. 

muquestionpapers.com hosts PDFs for most if not all previously asked question papers for Engineering in Mumbai University. The bot scrapes this website and sends the PDFs to the user directly on the Telegram app using the Telgram Bot API. 

Created this as a side-project to avoid opening a website and going through the steps everytime I wish to find a question paper. 

The bot is hosted online on Heroku.

## Getting started with Telegram Bots 

Chatbots are fun, and Telegram has one of the best APIs to make one. This project uses the python-telegram-bot wrapper which provides a Python interface for the Telegram API.

[Introduction to Telegram Bots](https://core.telegram.org/bots)

[Your First Bot using python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot)

## Run your own instance of MUQuestionPaperBot

1. Create a new bot with [BotFather](https://telegram.me/BotFather) and copy the API TOKEN 
2. Clone this repository
3. Run `pip install -U -r requirements.txt` to install the dependencies
4. Create a .env file in the `bots` directory with the following content:
    
    `TOKEN = your_token_here`
5. Set `DEBUG` to `True` in `telegram_bot.py`
6. Run `telegram_bot.py` 