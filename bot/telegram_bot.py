import os
import logging
import textwrap
from dotenv import load_dotenv

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters

from mu_functions import get_page, get_subjects, subject_list_to_message
from syllabus import dictionary

load_dotenv()
TOKEN = os.environ['TOKEN']
PORT = int(os.environ.get('PORT', '8443')) # Default port is 8443 if PORT isn't set
APP_NAME = os.environ['APP_NAME']

updater = Updater(TOKEN)
bot = telegram.Bot(TOKEN)
dispatcher = updater.dispatcher
print(bot.get_me()) 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

CHOOSE_BRANCH, CHOOSE_SEMESTER, CHOOSE_SUBJECT, SEND_DOCUMENTS = range(4)
SYLLABUS_YEAR, SEND_SYLLABUS = range(2)

def start(bot, update):
    """
    Sends initial message
    """
    message_text = textwrap.dedent("""
    Hi, I'm a bot that sends you PDFs of previous question papers for engineering in Mumbai University. 
    Use /question_paper to get the PDFs.
    Cancel with /cancel.
    """)
    bot.send_message(chat_id = update.message.chat_id, text = message_text) 

def question_paper(bot, update):
    """
    Entry point for the conversation to download question papers.
    Asks user to choose the particular year and semester to get the subjects for.
    """
    bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
    message_text = "Choose year"
    keyboard = [['FE'],['SE'],['TE'],['BE']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id = update.message.chat_id, text = message_text, reply_markup = reply_markup)

    return CHOOSE_BRANCH


def choose_branch(bot, update, user_data):
    """
    Asks user to choose the branch to get the questions papers for. 
    """
    if update.message.text == "/cancel":
        return ConversationHandler.END
    
    else:
        user_data['year'] = update.message.text
        bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
        message_text = "Choose branch"
        keyboard = [['Comps', 'IT', 'Extc'], ['Civil', 'Mechanical']]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        bot.send_message(chat_id = update.message.chat_id, text = message_text, reply_markup = reply_markup)

        return CHOOSE_SEMESTER
    

def choose_semester(bot, update, user_data):
    """
    Asks user to choose the semester to get the questions papers for.
    """
    if update.message.text == "/cancel":
        return ConversationHandler.END
    
    else:
        user_data['branch'] = update.message.text
        bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
        message_text = "Choose semester"
        
        keyboard = []
        if user_data['year'] =='FE':
            keyboard = [['Sem1'], ['Sem2']]
        elif user_data['year'] == 'SE':
            keyboard = [['Sem3'],['Sem4']]
        elif user_data['year'] == 'TE':
            keyboard = [['Sem5'],['Sem6']]
        elif user_data['year'] == 'BE':
            keyboard = [['Sem7'],['Sem8']]

        reply_markup = ReplyKeyboardMarkup(keyboard)
        bot.send_message(chat_id = update.message.chat_id, text = message_text, reply_markup = reply_markup)

        return CHOOSE_SUBJECT


def choose_subject(bot, update, user_data):
    """
    Fetches the pdf list for the chosen subject and sends them to the user.
    """
    if update.message.text == "/cancel":
        return ConversationHandler.END

    else:
        user_data['semester'] = update.message.text
        base_url = "https://muquestionpapers.com/"
        
        if user_data['year'] == 'FE':
            page_url = base_url + user_data['year'] + user_data['semester'] + ".php"
            
        else:
            page_url = base_url + user_data['year'] + user_data['branch'] + user_data['semester'] + ".php" 
            
        user_data['page'] = get_page(page_url)
        subject_list = get_subjects(user_data['page'])
        message_text = subject_list_to_message(subject_list)
        bot.send_message(chat_id = update.message.chat_id, text = message_text, reply_markup = ReplyKeyboardRemove()) 

        return SEND_DOCUMENTS


def send_documents(bot, update, user_data):
    """
    Gets links for the specified subject and sends the PDFs to the user. 
    """
    if update.message.text == "/cancel":
        return ConversationHandler.END

    else:
        user_data['subject'] = update.message.text[1:]
        index = int(user_data['subject'])
        tables = user_data['page'].find_all('table')
        all_links = tables[index].find_all('a')     
        download_links = []
        for link in all_links:
            download_links.append("https://muquestionpapers.com/" + link.get('href'))
        for download_link in download_links:
            bot.send_document(chat_id = update.message.chat_id, document = download_link)

        return ConversationHandler.END


def syllabus(bot, update):
    """
    Entry point for the conversation to download syllabus.
    Asks user to choose the particular branch to get the syllabus for.
    """
    bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
    message_text = "Choose branch"
    keyboard = [['Comps', 'IT', 'Extc'], ['Civil', 'Mechanical']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    bot.send_message(chat_id = update.message.chat_id, text = message_text, reply_markup = reply_markup)

    return SYLLABUS_YEAR


def syllabus_branch(bot, update, user_data):
    if update.message.text == "/cancel":
        return ConversationHandler.END

    else:
        user_data["Branch"] = update.message.text
        message_text = "Choose syllabus"
        keyboard = [[key] for key in dictionary[user_data["Branch"]]]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        bot.send_message(chat_id = update.message.chat_id, text = message_text, reply_markup = reply_markup)
        return SEND_SYLLABUS


def send_syllabus(bot, update, user_data):
    if update.message.text == "/cancel":
        return ConversationHandler.END

    else:
        user_data["syllabus"] = update.message.text
        syllabus_link = dictionary[user_data["Branch"]][user_data["syllabus"]]
        bot.send_message(chat_id = update.message.chat_id, text = user_data["syllabus"], reply_markup = ReplyKeyboardRemove())
        bot.send_document(chat_id = update.message.chat_id, document = syllabus_link)
        return ConversationHandler.END


def cancel(bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = "Cancelled", reply_markup = ReplyKeyboardRemove())
    
    return ConversationHandler.END    


def main():
    # handlers
    start_handler = CommandHandler('start', start)

    question_handler = ConversationHandler(
        entry_points = [CommandHandler('question_paper', question_paper)],
        
        states = {
            CHOOSE_BRANCH: [MessageHandler(Filters.text, callback = choose_branch, pass_user_data=True)],
            CHOOSE_SEMESTER: [MessageHandler(Filters.text, callback = choose_semester, pass_user_data=True)],
            CHOOSE_SUBJECT: [MessageHandler(Filters.text, callback = choose_subject, pass_user_data=True)],
            SEND_DOCUMENTS: [MessageHandler(Filters.command | Filters.text, callback = send_documents, pass_user_data=True)]
        },

        fallbacks = [CommandHandler('cancel', cancel)]
    )

    syllabus_handler = ConversationHandler(
        entry_points = [CommandHandler('syllabus', syllabus)],

        states = {
            SYLLABUS_YEAR: [MessageHandler(Filters.text, callback = syllabus_branch, pass_user_data=True)],
            SEND_SYLLABUS: [MessageHandler(Filters.text, callback = send_syllabus, pass_user_data=True)]
        },

        fallbacks = [CommandHandler('cancel', cancel)]
    )
    
    
    #dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(question_handler)
    dispatcher.add_handler(syllabus_handler)
    
    if DEBUG:
        updater.start_polling(clean=True)
        updater.idle()
    else:
        webhook_url = "https://{}.azurewebsites.net/{}".format(APP_NAME, TOKEN)
        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN)
        updater.bot.set_webhook(webhook_url)
        updater.idle()


if __name__ == '__main__':
    DEBUG = False       #When testing locally, change this to True
    main()
