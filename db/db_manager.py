import sqlite3
from datetime import datetime

DB_PATH = "data/diario_alimentare.sqlite"

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