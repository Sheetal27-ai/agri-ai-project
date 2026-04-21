import sqlite3

def init_db():
    conn = sqlite3.connect("agri.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        N INTEGER,
        P INTEGER,
        K INTEGER,
        ph REAL,
        temperature REAL,
        humidity REAL,
        rainfall REAL,
        best_crop TEXT,
        top_crops TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_prediction(soil, weather, result):
    conn = sqlite3.connect("agri.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions 
    (N, P, K, ph, temperature, humidity, rainfall, best_crop, top_crops)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        soil["N"],
        soil["P"],
        soil["K"],
        soil["ph"],
        weather["temperature"],
        weather["humidity"],
        weather["rainfall"],
        result["best_crop"],
        ",".join(result["top_crops"])
    ))

    conn.commit()
    conn.close()