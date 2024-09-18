from telebot import TeleBot
from io import BytesIO
from image_manager import init_board, draw_board
import db
import ast

BASE_URL = 'images'
TOKEN = '7137134345:AAGGznKxyxxxrcu3FrVAxzMBd4puauyu0qk'
bot = TeleBot(TOKEN)
is_white = False
game_id = None
    
def convert_to_bytes(board):
    image_io = BytesIO()
    board.save(image_io, 'PNG')
    image_io.seek(0)
    return image_io


@bot.message_handler(commands=['create_game'])
def create_game(message):
    global game_id, is_white
    game_id = db.create_game(message.from_user.id)
    bot.send_message(message.from_user.id, 'Вы создали игру с id: ' + game_id)
    board, init_pos = init_board()
    db.create_game_state(game_id, 0, init_pos)
    bot.send_photo(message.chat.id, convert_to_bytes(board))
    is_white = True


@bot.message_handler(commands=['join_game'])
def join_game(message):
    global game_id, is_white
    _, game_id = message.text.split(' ')
    if db.game_full(game_id):
        bot.send_message(message.chat.id, 'Игра уже началась')
        return
    db.join_game(message.from_user.id, game_id)
    bot.send_message(message.chat.id, 'Вы присоединились к игре с id: ' + message.text)
    is_white = False
    white_user_id = db.get_user_id(game_id, 'white')
    if white_user_id:
        bot.send_message(white_user_id[0], 'К игре присоединился игрок ' + message.from_user.first_name)


@bot.message_handler(commands=['move'])
def move(message):
    msg = message.text.split(' ')
    if len(msg) != 3:
        bot.send_message(message.chat.id, 'Неверный формат ввода должно быть /move A2 A4')
    user_black_id, user_white_id = db.user_ids(game_id)
    is_next_black, game_state = db.get_game_state(game_id)
    if bool(is_next_black) != (user_black_id == message.from_user.id): 
        bot.send_message(message.chat.id, 'Сейчас не ваш ход')
        return
    game_state = ast.literal_eval(game_state)
    _, move_from, move_to = message.text.split(' ')
    if move_from not in game_state:
        bot.send_message(message.chat.id, 'В этой клетке нет фигуры')
        return
    game_state[move_to] = game_state[move_from]
    del game_state[move_from]
    db.update_game_state(game_id, int(not user_black_id == message.from_user.id), game_state)
    board = draw_board(game_state)
    bot.send_photo(user_white_id, convert_to_bytes(board))
    bot.send_photo(user_black_id, convert_to_bytes(board))
    
    
    
if __name__ == '__main__':
    bot.polling(none_stop=True)