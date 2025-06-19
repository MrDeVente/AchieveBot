from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    # Путь к твоей директории проекта внутри Replit
    repo_path = os.getcwd()

    # Задай адрес репо через токен (см. ниже!)
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    REPO_URL = f'https://{GITHUB_TOKEN}@github.com/ТВОЙ_ЮЗЕРНЕЙМ/ТВОЙ_РЕПО.git'

    try:
        # Переход в папку проекта
        os.chdir(repo_path)

        # Если папка пустая — делаем clone
        if not os.path.exists('.git'):
            subprocess.run(['git', 'clone', REPO_URL, '.'], check=True)
        else:
            subprocess.run(['git', 'pull', 'origin', 'main'], check=True)

        # Перезапускаем приложение Replit (kill 1 — стандартный способ)
        os.system("kill 1")

        return '✅ Обновлено из GitHub и перезапущено!', 200

    except Exception as e:
        return f'❌ Ошибка: {str(e)}', 500

app.run(host='0.0.0.0', port=8080)

# pfvtsfr er

