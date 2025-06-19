from flask import Flask, request, jsonify
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # Путь к корню проекта
from bot import database  # Исправленный импорт

app = Flask(__name__)

@app.route("/achievements", methods=["GET"])
def get_achievements():
    user_id = request.args.get("user_id")
    return jsonify(database.get_achievements(user_id))

if __name__ == "__main__":
    database.init_db()  # Создаем таблицу при запуске сервера
    app.run(port=5000)