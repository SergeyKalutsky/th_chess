from telebot import TeleBot
from io import BytesIO
from image_manager import init_board
import db

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
    
    
@bot.message_handler(commands=['create_game'])
def create_game(message):
    game_id = db.create_game(message.from_user.id)
    bot.send_message(message.from_user.id, 'Вы создали игру с id: ' + game_id)


@bot.message_handler(commands=['join_game'])
def join_game(message):
    _, game_id = message.text.split(' ')
    if db.game_full(game_id):
        bot.send_message(message.chat.id, 'Игра уже началась')
        return
    db.join_game(message.from_user.id, game_id)
    bot.send_message(message.chat.id, 'Вы присоединились к игре с id: ' + message.text)
    white_user_id = db.get_user_id(game_id, 'white')
    if white_user_id:
        bot.send_message(white_user_id[0], 'К игре присоединился игрок ' + message.from_user.first_name)
    
    
if __name__ == '__main__':
    bot.polling(none_stop=True)