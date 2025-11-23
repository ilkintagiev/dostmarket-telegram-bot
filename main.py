import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from supabase import create_client
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = '7947192232:AAFqgzt57L2uRv2C-8pSs4OO-u584Kad3HU'
SUPABASE_URL = 'https://pishvfhkzsxjvddztcaa.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpc2h2ZmhrenpzeGp2ZGR6dGFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3NDkyNzAsImV4cCI6MTc0NjMyMjg3MH0.zZf4l-cCQYHQgU3dRZjlBhDG2EgGFvH_BcD8qJ4pNkE'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - приветствие с кнопкой"""
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    # Сохраняем Telegram ID
    try:
        supabase.table('telegram_users').insert({
            'telegram_id': user_id,
            'first_name': first_name,
            'created_at': 'now()'
        }).execute()
    except:
        pass
    
    # Создаём кнопку "Открыть DOST Market"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="🚀 Открыть DOST Market",
            web_app=WebAppInfo(url="https://dostmarket.online")
        )]
    ])
    
    # Отправляем приветствие
    await update.message.reply_text(
        f"🎉 Привет, {first_name}!\n\n"
        f"👋 Добро пожаловать в DOST Market!\n\n"
        f"🏪 Маркетплейс вещей которые дарят\n\n"
        f"✅ Раздай ненужные вещи\n"
        f"✅ Получи нужное\n"
        f"✅ Помогай друг другу\n\n"
        f"Нажми кнопку ниже чтобы начать!",
        reply_markup=keyboard
    )
    
    logger.info(f"Пользователь {user_id} ({first_name}) нажал /start")

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    main()
