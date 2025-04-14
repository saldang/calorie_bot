from db.schema import init_db
from scheduler.scheduler import start_scheduling

if __name__ == "__main__":
    init_db()
    from telegram.ext import ApplicationBuilder
    import os
    from dotenv import load_dotenv
    load_dotenv()

    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    # Hook per schedulazione
    start_scheduling(app)

    # Avvia bot
    from bot.telegram_bot import setup_handlers
    setup_handlers(app)
    print("✅ Bot e scheduler attivi.")
    app.run_polling()