import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "8045242125:AAGBXE5Ou_yXrGaKnzipe4tmV32PKAHnSw4"

# Фиксированный набор из 4 ссылок
LINKS = [
    ["🐲 Dragon Money", "https://drgnkk4.casino"],
    ["1️⃣ 1WIN", "https://1wldyd.com/casino/list?open=register&p=cnpz"],
    ["🦜 Martin", "https://martin-casino208.com"],
    ["🍾 Vodka", "https://sigma.vodka"]
]

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text=None):
    # Создаем клавиатуру с фиксированными ссылками
    keyboard = []
    for link in LINKS:
        keyboard.append([InlineKeyboardButton(link[0], url=link[1])])
    
    # Добавляем кнопки действий
    keyboard.append([
        InlineKeyboardButton("🔄 Обновить", callback_data="restart"),
        InlineKeyboardButton("📤 Поделиться", callback_data="share")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = message_text or "Актуальные зеркала:"
    
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_main_menu(update, context, "Добро пожаловать! Актуальные зеркала:")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "restart":
        # Просто обновляем меню с теми же ссылками
        await send_main_menu(update, context, "✅ Меню обновлено! Актуальные зеркала:")
    
    elif query.data == "share":
        bot_username = (await context.bot.get_me()).username
        
        share_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Поделиться ботом", url=f"https://t.me/share/url?url=https://t.me/{bot_username}&text=Всегда актуальные зеркала казино")],
            [InlineKeyboardButton("⬅️ Назад в меню", callback_data="restart")]
        ])
        
        await query.edit_message_text(
            f"📍 Поделитесь ботом с друзьями!\n\n"
            f"🔗 Ссылка: @{bot_username}\n\n"
            f"Нажмите кнопку ниже, чтобы сразу выбрать чат:",
            reply_markup=share_keyboard,
            parse_mode='HTML'
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
    
    print("🎉 Бот запущен!")
    print("📱 Напишите /start в Telegram")
    application.run_polling()

if __name__ == '__main__':
    main()