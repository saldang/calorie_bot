from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from llm.phi_interface import query_phi4
from db.db_manager import insert_pasto, get_last_7_days_summary, get_or_create_user
from utils.graphing import plot_calorie_summary
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = str(update.effective_chat.id)

    user_id = get_or_create_user(
        telegram_id=str(user.id),
        chat_id=chat_id,
        nome=user.first_name or "",
        cognome=user.last_name or ""
    )

    await update.message.reply_text(
        f"Ciao {user.first_name}! 🎉 Il tuo diario alimentare è stato attivato.\n"
        f"ID utente nel sistema: {user_id}\n\nScrivimi cosa hai mangiato oggi!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # TODO: in futuro estraiamo snippet da vector DB, per ora usiamo CSV statico
    csv_example = open("data/food_database.jsonl").read()[:3000]  # primi 3k caratteri

    try:
        result = query_phi4(user_text, csv_example)
        # Inseriamo un record generico per ora, dettagli alimenti = testo utente
        insert_pasto(
            user_id=1,
            alimento=user_text,  # oppure estratto da Phi-4, se hai parsing per alimento singolo
            quantita=100,        # placeholder: quantità media (migliorabile)
            kcal=result["kcal"],
            protein=result["proteins"],
            carbs=result["carbos"],
            fats=result["fats"]
        )
        await update.message.reply_text(
            f"🍽️ Totale stimato:\nCalorie: {result['kcal']} kcal\n"
            f"Proteine: {result['proteins']}g\n"
            f"Carboidrati: {result['carbos']}g\n"
            f"Grassi: {result['fats']}g"
        )
    except Exception as e:
        await update.message.reply_text(f"Errore nell'analisi del pasto: {e}")
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = 1  # da sostituire con gestione utenti vera
    data = get_last_7_days_summary(user_id)

    if not data:
        await update.message.reply_text("Nessun dato registrato negli ultimi 7 giorni.")
        return

    msg = "📊 Consumo calorico ultimi 7 giorni:\n"
    for date, kcal in data:
        msg += f"{date}: {int(kcal)} kcal\n"

    graph = plot_calorie_summary(data)
    await update.message.reply_photo(photo=graph, caption=msg)

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
