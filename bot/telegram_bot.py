import os
import logging
import textwrap
from dotenv import load_dotenv

import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters

from mu_functions import get_page, get_subjects, subject_list_to_message

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
    """
    Asks  user to choose the particular branch and semester to get the subjects for.
    """
    bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
    message_text = textwrap.dedent("""
    Choose your year:
    FE:
    /FESem1    /FESem2
    
    Comps:
    /SECompsSem3    /SECompsSem4
    /TECompsSem5    /TECompsSem6
    /BECompsSem7    /BECompsSem8
    
    IT:
    /SEITSem3    /SEITSem4
    /TEITSem5    /TEITSem6
    /BEITSem7    /BEITSem8

    EXTC:
    /SEExtcSem3    /SEExtcSem4
    /TEExtcSem5    /TEExtcSem6
    /BEExtcSem7    /BEExtcSem8

    Mechanical:
    /SEMechanicalSem3    /SEMechanicalSem4
    /TEMechanicalSem5    /TEMechanicalSem6
    /BEMechanicalSem7    /BEMechanicalSem8

    Civil:
    /SECivilSem3    /SECivilSem4
    /TECivilSem5    /TECivilSem6
    /BECivilSem7    /BECivilSem8
    """)
    bot.sendMessage(chat_id = update.message.chat_id, text = message_text)

    return CHOOSE_BRANCH


def choose_branch(bot, update, user_data):
    """
    Asks user to choose the subject to get the questions papers for. 
    """
    user_data['semester'] = update.message.text
    bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
    link = "https://muquestionpapers.com" + user_data['semester'] + ".php"
    page = get_page(link)
    user_data['page'] = page
    subject_list = get_subjects(page)
    user_data['subject_list'] = subject_list
    message_text = subject_list_to_message(subject_list)
    bot.send_message(chat_id = update.message.chat_id, text = message_text)

    return CHOOSE_SUBJECT
    

def choose_subject(bot, update, user_data):
    """
    Fetches the pdf list for the chosen subject and sends them to the user.
    """
    user_data['subject'] = update.message.text[1:]
    download_links = []
    tables = user_data['page'].find_all('table')
    index = int(user_data['subject'])
    all_links = tables[index].find_all('a')     
    for link in all_links:
        download_links.append("https://muquestionpapers.com/" + link.get('href'))
    for download_link in download_links:
        bot.send_document(chat_id = update.message.chat_id, document = download_link)
    
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

