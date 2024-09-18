from telebot import TeleBot
from io import BytesIO
from image_manager import init_board

BASE_URL = 'images'
TOKEN = '7137134345:AAGGznKxyxxxrcu3FrVAxzMBd4puauyu0qk'
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!')
    board = init_board()
    image_io = BytesIO()
    board.save(image_io, 'PNG')
    image_io.seek(0)
    bot.send_photo(message.chat.id, image_io)



if __name__ == '__main__':
    bot.polling(none_stop=True)