from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from typing import Dict

app = FastAPI()
DB_PATH = 'ab-tests.db'

class Event(BaseModel):
    experiment: str
    variant: str
    goal: str

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, experiment TEXT, variant TEXT, goal TEXT, timestamp TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS experiment_state (experiment TEXT PRIMARY KEY, winner TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.post('/events')
def log_event(event: Event):
    conn = get_conn()
    conn.execute('INSERT INTO events (experiment,variant,goal,timestamp) VALUES (?,?,?,?)',(event.experiment,event.variant,event.goal,datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return {'status':'ok'}

@app.get('/results/cta_test')
def results() -> Dict[str, Dict[str, float]]:
    conn = get_conn()
    cur = conn.cursor()
    variants=['A','B','C']
    data={}
    for v in variants:
        cur.execute('SELECT COUNT(*) FROM events WHERE experiment=? AND variant=? AND goal="view"',["cta_test",v])
        views = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM events WHERE experiment=? AND variant=? AND goal="click"',["cta_test",v])
        conv = cur.fetchone()[0]
        rate = (conv/views) if views else 0
        data[v]={'views':views,'conversions':conv,'rate':rate}
    conn.close()
    return data

@app.put('/results/cta_test/publish')
def publish(body: Dict[str,str]):
    variant = body.get('variant')
    if variant not in ['A','B','C']:
        raise HTTPException(status_code=400, detail='invalid variant')
    conn = get_conn()
    conn.execute('INSERT OR REPLACE INTO experiment_state (experiment,winner) VALUES (?,?)',["cta_test",variant])
    conn.commit()
    conn.close()
    return {'winner': variant}
