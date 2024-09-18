from telebot import TeleBot
from io import BytesIO
from image_manager import init_board, draw_board, add_endgame_text
from move_check import is_valid_move, is_checkmate, is_check
import db
import ast

BASE_URL = 'images'
TOKEN = '7137134345:AAGGznKxyxxxrcu3FrVAxzMBd4puauyu0qk'
bot = TeleBot(TOKEN)
is_white = False
game_id = '3fd86e64-c8bc-433f-a3a3-db8e14515f9d'
    
def convert_to_bytes(board):
    image_io = BytesIO()
    board.save(image_io, 'PNG')
    image_io.seek(0)
    return image_io


@bot.message_handler(commands=['create_game'])
def create_game(message):
    global game_id
    game_id = db.create_game(message.from_user.id)
    bot.send_message(message.from_user.id, 'Вы создали игру с id: ' + game_id)
    board, init_pos = init_board()
    db.create_game_state(game_id, 0, init_pos)
    bot.send_photo(message.chat.id, convert_to_bytes(board))


@bot.message_handler(commands=['join_game'])
def join_game(message):
    global game_id
    _, game_id = message.text.split(' ')
    if db.game_full(game_id):
        bot.send_message(message.chat.id, 'Игра уже началась')
        return
    db.join_game(message.from_user.id, game_id)
    bot.send_message(message.chat.id, 'Вы присоединились к игре с id: ' + message.text)
    white_user_id = db.get_user_id(game_id, 'white')
    if white_user_id:
        bot.send_message(white_user_id[0], 'К игре присоединился игрок ' + message.from_user.first_name)


@bot.message_handler(commands=['move'])
def move(message):
    global game_id
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
    if not is_valid_move(game_state, move_from, move_to):
        bot.send_message(message.chat.id, 'Недопустимый ход')
        return
    game_state[move_to] = game_state[move_from]
    del game_state[move_from]
    db.update_game_state(game_id, int(not user_black_id == message.from_user.id), game_state)
    board = draw_board(game_state)
    if is_checkmate(game_state, 'white'):
        board = add_endgame_text(board)
        bot.send_message(user_white_id, 'Белые проиграли')
        bot.send_message(user_black_id, 'Белые проиграли')
        game_id = None
    if is_checkmate(game_state, 'black'):
        board = add_endgame_text(board)
        bot.send_message(user_white_id, 'Черные проиграли')
        bot.send_message(user_black_id, 'Черные проиграли')
        game_id = None
    if is_check(game_state, 'white'):
        bot.send_message(user_white_id, 'Шах черным')
    if is_check(game_state, 'black'):
        bot.send_message(user_black_id, 'Шах белым')
    bot.send_photo(user_white_id, convert_to_bytes(board))
    bot.send_photo(user_black_id, convert_to_bytes(board))
    
    
    
if __name__ == '__main__':
    bot.polling(none_stop=True)