from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

EXPERIMENT = 'cta_test'
VARIANTS = ['A','B','C']


def get_conn():
    return sqlite3.connect('ab_events.db')

@router.get('/results/cta_test')
def results():
    conn = get_conn()
    cur = conn.cursor()
    data = {}
    for v in VARIANTS:
        cur.execute('SELECT COUNT(*) FROM events WHERE experiment=? AND variant=?',
                    (EXPERIMENT, v))
        views = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM events WHERE experiment=? AND variant=? AND goal=?',
                    (EXPERIMENT, v, 'cta_click'))
        conv = cur.fetchone()[0]
        rate = f"{(conv/views*100):.1f}%" if views else '0%'
        data[v] = {'views': views, 'conversions': conv, 'rate': rate}
    conn.close()
    return data

@router.put('/results/cta_test/publish')
def publish(winner: str):
    if winner not in VARIANTS:
        raise HTTPException(status_code=400, detail='invalid variant')
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('REPLACE INTO experiment_state (experiment, winner) VALUES (?,?)',
                (EXPERIMENT, winner))
    conn.commit()
    conn.close()
    return {'winner': winner}
