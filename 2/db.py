import sqlite3
from uuid import uuid4

def init_db():
    # Эту функцию нужно вызвать один раз, чтобы создать таблицу
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()

    # Create the "games" table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            user_white_id INTEGER,
            user_black_id INTEGER,
            game_id TEXT,
            won TEXT
        )
    ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def create_game(user_white_id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    game_id = str(uuid4())
    cursor.execute(f'''
        INSERT INTO games (user_white_id, game_id)
        VALUES ({user_white_id}, '{game_id}')
    ''')
    conn.commit()
    conn.close()
    return game_id


def game_full(game_id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT user_white_id, user_black_id
        FROM games
        WHERE game_id = '{game_id}'
    ''')
    users = cursor.fetchone()
    none_or_empty_count = sum(1 for user in users if user is None or user == '')
    conn.close()
    return none_or_empty_count == 0


def join_game(user_black_id, game_id):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE games
        SET user_black_id = {user_black_id}
        WHERE game_id = '{game_id}'
    ''')
    conn.commit()
    conn.close()
    
    
def get_user_id(game_id, color):
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT user_{color}_id
        FROM games
        WHERE game_id = '{game_id}'
    ''')
    user_id = cursor.fetchone()
    conn.close()
    return user_id
