import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "8045242125:AAGBXE5Ou_yXrGaKnzipe4tmV32PKAHnSw4"

# Фиксированный набор из 4 ссылок
LINKS = [
    ["🐲 Dragon Money", "https://drgnkk4.casino"],
    ["1️⃣ 1WIN", "https://1wldyd.com/casino/list?open=register&p=cnpz"],
    ["🦜 Martin", "https://martin-casino208.com"],
    ["🍾 Vodka", "https://sigma.vodka"]
]

def send_main_menu(update, context, message_text=None):
    keyboard = []
    for link in LINKS:
        keyboard.append([InlineKeyboardButton(link[0], url=link[1])])
    
    keyboard.append([
        InlineKeyboardButton("🔄 Обновить", callback_data="restart"),
        InlineKeyboardButton("📤 Поделиться", callback_data="share")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = message_text or "Актуальные зеркала:"
    
    if update.callback_query:
        update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        update.message.reply_text(text, reply_markup=reply_markup)

def start(update, context):
    send_main_menu(update, context, "Добро пожаловать! Актуальные зеркала:")

def button_handler(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data == "restart":
        send_main_menu(update, context, "✅ Меню обновлено! Актуальные зеркала:")
    
    elif query.data == "share":
        bot_username = context.bot.username
        
        share_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 Поделиться ботом", url=f"https://t.me/share/url?url=https://t.me/{bot_username}&text=Всегда актуальные зеркала казино")],
            [InlineKeyboardButton("⬅️ Назад в меню", callback_data="restart")]
        ])
        
        query.edit_message_text(
            f"📍 Поделитесь ботом с друзьями!\n\n"
            f"🔗 Ссылка: @{bot_username}\n\n"
            f"Нажмите кнопку ниже, чтобы сразу выбрать чат:",
            reply_markup=share_keyboard
        )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start))
    
    print("🎉 Бот запущен!")
    print("📱 Напишите /start в Telegram")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
