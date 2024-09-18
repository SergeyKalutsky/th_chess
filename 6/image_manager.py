from PIL import Image, ImageDraw, ImageFont
import json

OFFSET = 35

letters_map = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7
}


def translate_position(position):
    x = letters_map[position[0].upper()]
    y = 8 - int(position[1])
    return x, y


def place_figure(figure, position, board):
    chess_piece = Image.open(f'images/{figure}.png')
    x, y = translate_position(position)
    board.paste(chess_piece, (OFFSET+(x*60), OFFSET+(y*60)), chess_piece)
    return board


def init_board():
    board = Image.open('images/board.png')
    with open('init_positions.json') as f:
        init_positions = json.load(f)
    for position, figure in init_positions.items():
        board = place_figure(figure, position, board)
    return board, init_positions


def draw_board(game_state):
    board = Image.open('images/board.png')
    for position, figure in game_state.items():
        board = place_figure(figure, position, board)
    return board

def add_endgame_text(board):
    draw = ImageDraw.Draw(board)
    font = ImageFont.truetype('Times New Roman.ttf', 80)
    text = "Шах и мат"
    text_width, text_height = draw.textsize(text, font=font)
    width, height = board.size
    position = ((width - text_width) / 2, (height - text_height) / 2)
    draw.text(position, text, (0, 0, 0), font=font, encoding='utf-8')
    return board