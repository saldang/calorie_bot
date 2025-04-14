import sqlite3

DB_PATH = "data/diario_alimentare.sqlite"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS utenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE,
        nome TEXT,
        cognome TEXT,
        altezza_cm INTEGER,
        peso_kg REAL,
        sesso TEXT,
        data_nascita TEXT,
        stile_vita TEXT,
        fabbisogno_calorico REAL,
        percentuale_riduzione INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pasti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utente_id INTEGER,
        data TEXT,
        alimento TEXT,
        quantita_grammi REAL,
        calorie REAL,
        proteine REAL,
        carboidrati REAL,
        grassi REAL,
        FOREIGN KEY (utente_id) REFERENCES utenti(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pesi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utente_id INTEGER,
        data TEXT,
        peso_kg REAL,
        FOREIGN KEY (utente_id) REFERENCES utenti(id)
    )
    """)

    conn.commit()
    conn.close()