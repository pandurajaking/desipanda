import os
import telebot

bot = telebot.TeleBot("6309773140:AAFaxUDW3IQ9fHa8jkUCcCT2-3oYV5wikso")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hi! I can convert HTML files to text files.")
    bot.send_message(message.chat.id, "To convert an HTML file, send me the file.")

@bot.message_handler(content_types=["document"])
def handle_document(message):
    file_name = message.document.file_name
    file_content = message.document.file_id

    with open(file_name, "wb") as f:
        f.write(bot.get_file(file_content).download_as_file())

    text_content = convert_html_to_text(file_name)

    bot.send_message(message.chat.id, f"Here is the converted text file: {file_name}: {text_content}")

def convert_html_to_text(file_name):
    text = ""
    with open(file_name, "r") as f:
        for line in f:
            text += line

    return text

if __name__ == "__main__":
    bot.polling()
