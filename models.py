import sqlite3

def create_tables():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            Age INTEGER NOT NULL,
            Gender TEXT NOT NULL,
            Height REAL NOT NULL,
            Weight REAL NOT NULL,
            Avg_HR INTEGER NOT NULL,
            Physical_History INTEGER NOT NULL,
            Sleep_Duration INTEGER DEFAULT NULL,
            Quality_of_Sleep INTEGER DEFAULT NULL,
            Weight_Loss_Goal INTEGER DEFAULT NULL,
            Weight_Loss_Time INTEGER DEFAULT NULL,
            Distance INTEGER DEFAULT NULL,
            Calories INTEGER DEFAULT NULL,
            Time TEXT DEFAULT NULL,
            Speed TEXT DEFAULT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

create_tables()
