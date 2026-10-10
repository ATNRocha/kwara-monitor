
import sqlite3
from pathlib import Path
from contextlib import contextmanager
BASE=Path(__file__).resolve().parents[1]; DB=BASE/"data/kwara.db"
SCHEMA="""
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS snapshots(
id INTEGER PRIMARY KEY AUTOINCREMENT,captured_at TEXT NOT NULL,lot INTEGER NOT NULL,ref TEXT,title TEXT,value_type TEXT,
current_value REAL,bid_count INTEGER,increment REAL,next_bid REAL,displayed_total REAL,calculated_total REAL,end_at TEXT,
remaining_text TEXT,market_value REAL,max_bid REAL,tech_score REAL,aesthetic_score REAL,status TEXT,cb_index REAL,
raw_excerpt TEXT,parse_ok INTEGER NOT NULL DEFAULT 1,error TEXT);
CREATE INDEX IF NOT EXISTS idx_snapshots_lot_time ON snapshots(lot,captured_at DESC);
CREATE TABLE IF NOT EXISTS worker_status(id INTEGER PRIMARY KEY CHECK(id=1),updated_at TEXT,cycle_started_at TEXT,cycle_finished_at TEXT,
enabled_lots INTEGER,successes INTEGER,failures INTEGER,last_error TEXT);
"""
@contextmanager
def connect():
    DB.parent.mkdir(parents=True,exist_ok=True); con=sqlite3.connect(DB,timeout=30); con.row_factory=sqlite3.Row
    try: yield con; con.commit()
    finally: con.close()
def init_db():
    with connect() as c:c.executescript(SCHEMA)
def insert_snapshot(row):
    keys=["captured_at","lot","ref","title","value_type","current_value","bid_count","increment","next_bid","displayed_total","calculated_total","end_at","remaining_text","market_value","max_bid","tech_score","aesthetic_score","status","cb_index","raw_excerpt","parse_ok","error"]
    with connect() as c:c.execute(f"INSERT INTO snapshots({','.join(keys)}) VALUES({','.join('?' for _ in keys)})",[row.get(k) for k in keys])
def update_worker_status(**kw):
    if not kw:return
    with connect() as c:
        c.execute("INSERT OR IGNORE INTO worker_status(id) VALUES(1)")
        c.execute("UPDATE worker_status SET "+",".join(f"{k}=?" for k in kw)+" WHERE id=1",[kw[k] for k in kw])
