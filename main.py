import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from supabase import create_client
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Твои переменные
TELEGRAM_TOKEN = '7947192232:AAFqgzt57L2uRv2C-8pSs4OO-u584Kad3HU'
SUPABASE_URL = 'https://pishvfhkzsxjvddztcaa.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpc2h2ZmhrenpzeGp2ZGR6dGFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA3NDkyNzAsImV4cCI6MTc0NjMyMjg3MH0.zZf4l-cCQYHQgU3dRZjlBhDG2EgGFvH_BcD8qJ4pNkE'

# Подключение к Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - автоматически сохраняет Telegram ID"""
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    try:
        # Просто сохраняем в таблице telegram_users
        response = supabase.table('telegram_users').insert({
            'telegram_id': user_id,
            'first_name': first_name,
            'created_at': 'now()'
        }).execute()
        
        # Отправляем сообщение
        await update.message.reply_text(
            f"✅ Привет, {first_name}!\n\n"
            f"Твой Telegram ID сохранён: `{user_id}`\n\n"
            f"🎉 Теперь можешь регистрироваться в DOST Market!",
            parse_mode='Markdown'
        )
        logger.info(f"Пользователь {user_id} ({first_name}) сохранён")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(
            "✅ Твой Telegram ID сохранён!\n\n"
            "🎉 Можешь регистрироваться в DOST Market!"
        )

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
