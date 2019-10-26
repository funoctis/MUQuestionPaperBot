import os
import logging
import textwrap

from dotenv import load_dotenv
import telegram
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters

from question_paper import (question_paper, choose_branch, choose_semester, choose_subject, send_documents, 
                                CHOOSE_BRANCH, CHOOSE_SEMESTER, CHOOSE_SUBJECT, SEND_DOCUMENTS)
from syllabus import dictionary, syllabus, syllabus_branch, send_syllabus, SYLLABUS_YEAR, SEND_SYLLABUS

load_dotenv()
TOKEN = os.environ['TOKEN']
PORT = int(os.environ.get('PORT', '8443')) # Default port is 8443 if PORT isn't set
APP_NAME = os.environ.get('APP_NAME', "") # The "" is only to avoid error while debug, it'll never be used

updater = Updater(TOKEN)
bot = telegram.Bot(TOKEN)
dispatcher = updater.dispatcher
print(bot.get_me()) 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


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
        webhook_url = "https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN)
        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN)
        updater.bot.set_webhook(webhook_url)
        updater.idle()


if __name__ == '__main__':
    DEBUG = False      #When testing locally, change this to True
    main()
