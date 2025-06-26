from fastapi import FastAPI
from .routers import events, results
import sqlite3

app = FastAPI()

def get_db():
    conn = sqlite3.connect('ab_events.db')
    conn.row_factory = sqlite3.Row
    conn.execute('''CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment TEXT,
        variant TEXT,
        goal TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS experiment_state(
        experiment TEXT PRIMARY KEY,
        winner TEXT
    )''')
    return conn

@app.on_event('startup')
def startup():
    get_db().close()

app.include_router(events.router, prefix="")
app.include_router(results.router, prefix="")
