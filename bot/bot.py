import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
import database

BOT_TOKEN = os.getenv("7828949990:AAGFIP4CKWORxZeBJpV3LsnA_tpfNd0OUXY")  # Загружаем токен из переменных окружения


async def add_achievement(update: Update, context):
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите текст достижения после команды.")
        return
    user_id = update.effective_user.id
    achievement = " ".join(context.args)
    database.save_achievement(user_id, achievement)
    await update.message.reply_text(f"Достижение '{achievement}' добавлено!")


async def list_achievements(update: Update, context):
    user_id = update.effective_user.id
    items = database.get_achievements(user_id)
    if not items:
        text = "У вас ещё нет достижений."
    else:
        text = "Ваши достижения:\n" + "\n".join(f"– {a}" for a in items)
    await update.message.reply_text(text)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("add", add_achievement))
    app.add_handler(CommandHandler("list", list_achievements))
    app.run_polling()


if __name__ == "__main__":
    database.init_db()
    main()