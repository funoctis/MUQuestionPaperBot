import os
import logging
import requests
import textwrap
import telegram
from bs4 import BeautifulSoup
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters
from dotenv import load_dotenv
from mu_functions import get_subjects, subject_list_to_message

load_dotenv()
TOKEN = os.environ['TOKEN']
updater = Updater(TOKEN)
bot = telegram.Bot(TOKEN)
dispatcher = updater.dispatcher
print(bot.get_me()) 

CHOOSE_BRANCH, CHOOSE_SUBJECT = range(2)

def start(bot, update):
    """
    Sends initial message
    """
    print("Hello")
    message_text = "Hi, I'm a bot that sends you PDFs of previous question papers for engineering in Mumbai University"

    bot.send_message(chat_id = update.message.chat_id, text = message_text) 

def question_paper(bot, update):
    bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
    message_text = textwrap.dedent("""
    Choose your year:
    FE:
    /FESem1
    /FESem2
    
    Comps:
    /SECompsSem3
    /SECompsSem4
    /TECompsSem5
    /TECompsSem6
    /BECompsSem7
    /BECompsSem8

    IT:
    /SEITSem3
    /SEITSem4
    /TEITSem5
    /TEITSem6
    /BEITSem7
    /BEITSem8
    """)
    bot.sendMessage(chat_id = update.message.chat_id, text = message_text)

    return CHOOSE_BRANCH

def choose_branch(bot, update, user_data):
    user_data['semester'] = update.message.text
    bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
    print(user_data['semester'])
    link = "https://muquestionpapers.com" + user_data['semester'] + ".php"
    print(link)
    subject_list = get_subjects(link)
    print(subject_list)
    message_text = subject_list_to_message(subject_list)
    print(message_text)
    bot.send_message(chat_id = update.message.chat_id, text = message_text)

    return CHOOSE_SUBJECT
    

def choose_subject(bot, update, user_data):
    user_data['subject'] = update.message.text
    print(user_data['subject'])
    
    return ConversationHandler.END


def cancel(bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = "Cancelled")
    
    return ConversationHandler.END    



def main():
    question_handler = ConversationHandler(
        entry_points = [CommandHandler('question_paper', question_paper)],
        
        states = {
            CHOOSE_BRANCH: [MessageHandler(Filters.command, callback = choose_branch, pass_user_data=True)],
            CHOOSE_SUBJECT: [MessageHandler(Filters.command, callback = choose_subject, pass_user_data=True)]
        },

        fallbacks = [CommandHandler('cancel', cancel)]
    )
    
    
    # handlers
    start_handler = CommandHandler('start', start)
    
    
    #dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(question_handler)

    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

