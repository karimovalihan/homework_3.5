import sqlite3
from aiogram.fsm.state import State, StatesGroup

conn = sqlite3.connect('bank.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance REAL DEFAULT 0.0
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transfers (
        sender_id INTEGER,
        receiver_id INTEGER,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()


class MyStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_receiver = State()


def register_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0.0

def update_balance(user_id, amount):
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()

def create_transfer(sender_id, receiver_id, amount):
    cursor.execute("INSERT INTO transfers (sender_id, receiver_id, amount) VALUES (?, ?, ?)", 
                   (sender_id, receiver_id, amount))
    conn.commit()

def has_account(user_id):
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

def add_transfer(sender_id, receiver_id, amount):
    conn = sqlite3.connect('bank_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transfers (sender_id, receiver_id, amount) VALUES (?, ?, ?)', 
                   (sender_id, receiver_id, amount))
    conn.commit()
    conn.close()