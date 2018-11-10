import os
import logging
import requests
import telegram
from bs4 import BeautifulSoup
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ['TOKEN']
updater = Updater(TOKEN)
bot = telegram.Bot(TOKEN)
dispatcher = updater.dispatcher
print(bot.get_me())

def start(bot, update):
    """
    Sends initial message
    """
    print("Hello")
    message_text = "Hi, I'm a bot that sends you PDFs of previous question papers for engineering in Mumbai University"

    bot.send_message(chat_id=update.message.chat_id, text = message_text) 

def question_paper(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
    message_text = "/comps"
    bot.sendMessage(chat_id=update.message.chat_id, text=message_text)

def comps(bot, update):
    url = "https://muquestionpapers.com/SECompsSem3.php"
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'html.parser')

    headers = soup.find_all('th')
    urllist = list()
    i = 0
    
    for lines in headers:
        line = str(lines)
        if 'pdf' in line:
            line = line.split('"')[3]
            urllist.append(line)
            i+=1
    
    for download_link in urllist:
        base_url = "https://muquestionpapers.com"
        url = base_url + "/" + download_link
        bot.send_document(chat_id=update.message.chat_id, document=url)

# handlers
start_handler = CommandHandler('start', start)
question_paper_handler = CommandHandler('question_paper', question_paper)
comps_handler = CommandHandler('comps', comps)

#dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(question_paper_handler)
dispatcher.add_handler(comps_handler)


updater.start_polling()

