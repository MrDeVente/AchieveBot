import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import database
import re

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Environment variable BOT_TOKEN is not set.")

def build_keyboard(buttons):
    return InlineKeyboardMarkup([[btn] for btn in buttons])

async def add_achievement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /achieve "текст пользователя"
    text = update.message.text
    match = re.match(r'/achieve\s+([^"]+)', text)
    if not match:
        await update.message.reply_text('Используйте: /achieve "текст достижения"')
        return
    achievement = match.group(1)
    user_id = str(update.effective_user.id)
    database.save_achievement(user_id, achievement)
    await update.message.reply_text(f'Достижение "{achievement}" добавлено!')

async def reward_selector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /reward или /reward <id> "текст награды"
    args = context.args
    if not args:
        user_id = str(update.effective_user.id)
        items = database.get_unrewarded(user_id)
        if not items:
            return await update.message.reply_text('Нет достижений без награды.')
        buttons = [
            InlineKeyboardButton(f'{i+1}. {a[1]}', switch_inline_query_current_chat=f'/reward {a[0]} ')
            for i, a in enumerate(items)
        ]
        return await update.message.reply_text('Выберите достижение для награды:', reply_markup=build_keyboard(buttons))
    # Пользователь выбрал id, теперь ждём текст награды
    if len(args) < 2:
        return await update.message.reply_text('После кнопки допишите: /reward <id> "текст награды"')
    ach_id = args[0]
    reward_text = update.message.text.split(None, 2)[2].strip('"')
    database.set_reward(ach_id, reward_text)
    await update.message.reply_text(f'Награда для достижения {ach_id} установлена: "{reward_text}"')

async def rewrite_selector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /rewrite или /rewrite <subcmd> или /rewrite <subcmd> <id> "новый текст"
    args = context.args
    user_id = str(update.effective_user.id)

    if not args:
        # показать команды achieve и reward
        cmds = [
            InlineKeyboardButton('achieve', switch_inline_query_current_chat='/rewrite achieve '),
            InlineKeyboardButton('reward', switch_inline_query_current_chat='/rewrite reward '),
        ]
        return await update.message.reply_text('Выберите, что переписать:', reply_markup=build_keyboard(cmds))

    sub = args[0]
    if sub == 'achieve' and len(args) == 1:
        # список всех достижений
        items = database.get_all_achievements(user_id)
        buttons = [
            InlineKeyboardButton(f'{i+1}. {a["text"]}', switch_inline_query_current_chat=f'/rewrite achieve {a["id"]} ')
            for i, a in enumerate(items)
        ]
        return await update.message.reply_text('Выберите достижение для редактирования:', reply_markup=build_keyboard(buttons))

    if sub == 'reward' and len(args) == 1:
        # список награждённых достижений
        items = database.get_all_achievements(user_id)
        rewarded = [(a['id'], a['text']) for a in items if a['reward']]
        if not rewarded:
            return await update.message.reply_text('Нет награждённых достижений.')
        buttons = [
            InlineKeyboardButton(f'{i+1}. {text}', switch_inline_query_current_chat=f'/rewrite reward {id} ')
            for i, (id, text) in enumerate(rewarded)
        ]
        return await update.message.reply_text('Выберите награду для редактирования:', reply_markup=build_keyboard(buttons))

    # если указаны subcmd, id и новый текст
    if len(args) >= 3:
        ach_id = args[1]
        new_text = update.message.text.split(None, 3)[3].strip('"')
        if sub == 'achieve':
            database.update_achievement(ach_id, new_text)
            return await update.message.reply_text(f'Достижение {ach_id} изменено на "{new_text}"')
        elif sub == 'reward':
            database.set_reward(ach_id, new_text)
            return await update.message.reply_text(f'Награда {ach_id} изменена на "{new_text}"')

    await update.message.reply_text('Неверный формат. Используйте /rewrite')

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('achieve', add_achievement))
    app.add_handler(CommandHandler('reward', reward_selector))
    app.add_handler(CommandHandler('rewrite', rewrite_selector))
    app.run_polling()

if __name__ == '__main__':
    database.init_db()
    main()
