# Entry point per il bot e il sistema di scheduling
# main.py
from bot.telegram_bot import run_bot
from db.schema import init_db

if __name__ == "__main__":
    init_db()
    run_bot()
