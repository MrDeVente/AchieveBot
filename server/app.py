import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
from pathlib import Path

# Добавляем корень проекта в sys.path
sys.path.append(str(Path(__file__).parent.parent))
from bot import database

app = Flask(
    __name__,
    static_folder=str(Path(__file__).parent.parent / 'web_app'),
    static_url_path=''
)
CORS(app)

database.init_db()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/achievements', methods=['GET'])
def achievements_api():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    items = database.get_all_achievements(user_id)
    return jsonify(items)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)