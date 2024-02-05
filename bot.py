from telegram import Update, Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import re

TOKEN = '6488165968:AAFyogItsIQm2VEsk_GWRsZAXf3ZNij-t6s'
bot = Bot(TOKEN)
updater = Updater(bot=bot)

def start(update: Update, context):
    update.message.reply_text('Hello! Send me a text or .txt file, and I will extract names and URLs, then format them as name:https url. I will send you back the modified text as a .txt file.')

def handle_document(update: Update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.txt')
    with open('temp.txt', 'r') as f:
        text = f.read()
    formatted_text = format_text(text)
    with open('formatted_text.txt', 'w') as f:
        f.write(formatted_text)
    with open('formatted_text.txt', 'rb') as f:
        context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(f), filename='formatted_text.txt')
    os.remove('temp.txt')
    os.remove('formatted_text.txt')

def format_text(text):
    lines = text.split('\n')
    formatted_lines = []
    current_name = ""
    
    # Lines already in "name:https" format will be preserved in the final output
    existing_lines = [line for line in lines if re.match(r'.+:https://[^\s]+', line)]
    formatted_lines.extend(existing_lines)
    
    for line in lines:
        url_matches = re.findall(r'https://[^\s]+', line)
        for url_match in url_matches:
            url = url_match.strip()
            name = current_name if current_name and ':' not in current_name else 'no name'
            formatted_line = f'{name}:{url}'
            if formatted_line not in formatted_lines:  # Ensure unique pairs
                formatted_lines.append(formatted_line)
                current_name = ""  # Reset current_name for the next URL
    return '\n'.join(formatted_lines)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

updater.start_polling()
updater.idle()
