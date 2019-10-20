from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

SYLLABUS_YEAR, SEND_SYLLABUS = range(2)

branches = ["Comps", "Civil", "IT", "Extc", "Mechanical"]

syllabi = [{"Second Year (S.E.) Semester 3&4 (Choice Based)":"https://muquestionpapers.com/download/syllabus/Comps/SE-Comps_CBCGS_Syllabus.pdf",
           "T.E. & B.E. Semester 5 to Sem 8 Syllabus (Choice Based)":"https://muquestionpapers.com/download/syllabus/Comps/TE_BE-Comp_Engg_CBCGS_Syllabus.pdf",},          
           {"Second Year (S.E.) Semester 3&4 (Choice Based)":"https://muquestionpapers.com/download/syllabus/CIVIL/SE-Civil_CBCGS_Syllabus.pdf",
           "Third Year (T.E.) Semester 3&4 (Choice Based)":"https://muquestionpapers.com/download/syllabus/CIVIL/TE-Civil_CBCGS_Syllabus.pdf"},            
           {"S.E. to B.E. Semester 3 to Semester 8 Syllabus (Choice Based)":"https://muquestionpapers.com/download/syllabus/IT/SE%20to%20BE-IT_CBCGS_Syllabus.pdf"},           
           {"Second Year (S.E.) Semester 3&4 (Choice Based)":"https://muquestionpapers.com/download/syllabus/EXTC/SE-EXTC_CBCGS_Syllabus.pdf",
            "T.E. & B.E. Semester 5 to Sem 8 Syllabus (Choice Based)":"https://muquestionpapers.com/download/syllabus/EXTC/TE_BE-EXTC_CBCGS_Syllabus.pdf"},           
           {"S.E. to B.E. Semester 3 to Semester 8 Syllabus (Choice Based)":"https://muquestionpapers.com/download/syllabus/MECHANICAL/SE%20to%20BE-Mechanical_CBCGS_Syllabus.pdf"}
        ]

dictionary = dict(zip(branches, syllabi))

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
