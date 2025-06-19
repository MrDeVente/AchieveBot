from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
import database  # Исправленный импорт

async def add_achievement(update: Update, context):
    user_id = update.effective_user.id
    achievement = " ".join(context.args)
    database.save_achievement(user_id, achievement)
    await update.message.reply_text(f"Достижение '{achievement}' добавлено!")

def main():
    app = ApplicationBuilder().token("7828949990:AAGFIP4CKWORxZeBJpV3LsnA_tpfNd0OUXY").build()
    app.add_handler(CommandHandler("add", add_achievement))
    app.run_polling()

if __name__ == "__main__":
    database.init_db()  # Создаем таблицу при запуске бота
    main()