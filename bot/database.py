import sqlite3

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS achievements (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, text TEXT, reward TEXT)"
        )

def save_achievement(user_id, text):
    with sqlite3.connect("database.db") as conn:
        conn.execute(
            "INSERT INTO achievements (user_id, text, reward) VALUES (?, ?, NULL)",
            (user_id, text),
        )

def get_all_achievements(user_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.execute(
            "SELECT id, text, reward FROM achievements WHERE user_id=?", (user_id,)
        )
        return [
            {'id': row[0], 'text': row[1], 'reward': row[2]}
            for row in cursor.fetchall()
        ]

def get_unrewarded(user_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.execute(
            "SELECT id, text FROM achievements WHERE user_id=? AND reward IS NULL", (user_id,)
        )
        return cursor.fetchall()

def set_reward(ach_id, reward):
    with sqlite3.connect("database.db") as conn:
        conn.execute(
            "UPDATE achievements SET reward=? WHERE id=?",
            (reward, ach_id),
        )
        