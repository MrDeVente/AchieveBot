import sqlite3

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS achievements (user_id TEXT, achievement TEXT)")

def save_achievement(user_id, achievement):
    with sqlite3.connect("database.db") as conn:
        conn.execute("INSERT INTO achievements VALUES (?, ?)", (user_id, achievement))

def get_achievements(user_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.execute("SELECT achievement FROM achievements WHERE user_id=?", (user_id,))
        return [row[0] for row in cursor.fetchall()]