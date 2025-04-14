from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from llm.phi_interface import query_phi4
from db.db_manager import insert_pasto

import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Ciao {user.first_name}! Benvenuto nel tuo diario alimentare 🥗\nScrivimi cosa hai mangiato oggi!"
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

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot avviato. In attesa di messaggi...")
    app.run_polling()
