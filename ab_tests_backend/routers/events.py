from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3

router = APIRouter()

class Event(BaseModel):
    experiment: str
    variant: str
    goal: str


def get_conn():
    return sqlite3.connect('ab_events.db')

@router.post('/events')
def save_event(event: Event):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO events (experiment, variant, goal) VALUES (?,?,?)',
                (event.experiment, event.variant, event.goal))
    conn.commit()
    conn.close()
    return {'status': 'ok'}
