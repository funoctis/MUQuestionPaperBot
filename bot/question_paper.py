from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from mu_functions import get_page, get_subjects, subject_list_to_message

CHOOSE_BRANCH, CHOOSE_SEMESTER, CHOOSE_SUBJECT, SEND_DOCUMENTS = range(4)

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