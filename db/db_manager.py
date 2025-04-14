import sqlite3
from datetime import datetime, timedelta

DB_PATH = "data/diario_alimentare.sqlite"


def get_or_create_user(telegram_id: str, chat_id: str, nome: str, cognome: str = "") -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se esiste
    cursor.execute("SELECT id FROM utenti WHERE telegram_id = ?", (telegram_id,))
    row = cursor.fetchone()

    if row:
        # Aggiorna eventuale chat_id
        cursor.execute("UPDATE utenti SET chat_id = ? WHERE telegram_id = ?", (chat_id, telegram_id))
        conn.commit()
        conn.close()
        return row[0]
    else:
        cursor.execute("""
            INSERT INTO utenti (telegram_id, chat_id, nome, cognome)
            VALUES (?, ?, ?, ?)
        """, (telegram_id, chat_id, nome, cognome))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

def insert_pasto(user_id: int, alimento: str, quantita: float, kcal: float, protein: float, carbs: float, fats: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pasti (utente_id, data, alimento, quantita_grammi, calorie, proteine, carboidrati, grassi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        datetime.now().strftime("%Y-%m-%d"),
        alimento,
        quantita,
        kcal,
        protein,
        carbs,
        fats
    ))
    conn.commit()
    conn.close()

def get_last_7_days_summary(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    start_date = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT data, SUM(calorie)
        FROM pasti
        WHERE utente_id = ? AND data >= ?
        GROUP BY data
        ORDER BY data
    """, (user_id, start_date))

    results = cursor.fetchall()
    conn.close()

    return results  # [(data, calorie), ...]