from db.db_manager import get_last_7_days_summary
from utils.graphing import plot_calorie_summary
import sqlite3

DB_PATH = "data/diario_alimentare.sqlite"


def get_all_user_chat_ids():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, chat_id FROM utenti WHERE chat_id IS NOT NULL")
    return cursor.fetchall()


async def send_report_to_user(bot, chat_id: int, user_id: int):
    data = get_last_7_days_summary(user_id)
    if not data:
        await bot.send_message(chat_id=chat_id, text="Nessun dato disponibile per oggi.")
        return

    msg = "📊 Report giornaliero - calorie ultimi 7 giorni:\n"
    for date, kcal in data:
        msg += f"{date}: {int(kcal)} kcal\n"

    graph = plot_calorie_summary(data)
    await bot.send_photo(chat_id=chat_id, photo=graph, caption=msg)



def send_daily_report(bot_app):
    user_list = get_all_user_chat_ids()  # [(user_id, chat_id)]

    for user_id, chat_id in user_list:
        if chat_id:
            bot_app.create_task(send_report_to_user(bot_app.bot, chat_id, user_id))