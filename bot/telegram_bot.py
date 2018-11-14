import os
import logging
import textwrap
from dotenv import load_dotenv

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters

from mu_functions import get_page, get_subjects, subject_list_to_message

load_dotenv()
TOKEN = os.environ['TOKEN']
updater = Updater(TOKEN)
bot = telegram.Bot(TOKEN)
dispatcher = updater.dispatcher
print(bot.get_me()) 

CHOOSE_BRANCH, CHOOSE_SEMESTER, CHOOSE_SUBJECT, SEND_DOCUMENTS = range(4)

def start(bot, update):
    """
    Sends initial message
    """
    
    message_text = "Hi, I'm a bot that sends you PDFs of previous question papers for engineering in Mumbai University"
    bot.send_message(chat_id = update.message.chat_id, text = message_text) 

def question_paper(bot, update):
    """
    Asks  user to choose the particular year to get the subjects for.
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
    
    elif update.message.text == 'FE':
        user_data['year'] = update.message.text
        return CHOOSE_SEMESTER
    
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
    
    elif user_data['year'] == 'FE':
        keyboard = [['Sem1'], ['Sem2']]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        message_text = "Choose semester"
        bot.send_message(chat_id = update.message.chat_id, text = message_text, reply_markup = reply_markup)

    else:
        user_data['branch'] = update.message.text
        bot.send_chat_action(chat_id = update.message.chat_id, action = 'typing')
        message_text = "Choose semester"
        keyboard = [['Sem3', 'Sem4'], ['Sem5', 'Sem6'], ['Sem7', 'Sem8']]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        bot.send_message(chat_id = update.message.chat_id, text = message_text, reply_markup = reply_markup)

        return CHOOSE_SUBJECT


def choose_subject(bot, update, user_data):
    """
    Asks user to choose the subject to get the questions papers for.
    """
    if update.message.text == "/cancel":
        return ConversationHandler.END
    
    else:
        user_data['semester'] = update.message.text
        base_url = "https://muquestionpapers.com/"
        page_url = base_url + user_data['year'] + user_data['branch'] + user_data['semester'] + ".php" 
        user_data['page'] = get_page(page_url)
        subject_list = get_subjects(user_data['page'])
        message_text = subject_list_to_message(subject_list)
        bot.send_message(chat_id = update.message.chat_id, text = message_text, reply_markup = ReplyKeyboardRemove()) 

        return SEND_DOCUMENTS


def send_documents(bot, update, user_data):
    """
    Finds download links for the user selected subject and sends the documents hosted at these links to the user.
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


def cancel(bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = "Cancelled")
    
    return ConversationHandler.END    



def main():
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
    
    
    # handlers
    start_handler = CommandHandler('start', start)
    
    
    #dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(question_handler)

    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
