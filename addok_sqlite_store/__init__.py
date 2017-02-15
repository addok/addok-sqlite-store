import os
import sqlite3
from multiprocessing import Lock

from addok.config import config


class SQLiteStore:

    def __init__(self, *args, **kwargs):
        self.init()

    def init(self):
        self.conn = sqlite3.connect(config.SQLITE_DB_PATH)
        self.lock = Lock()
        with self.conn as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS '
                         'addok (key VARCHAR, data BLOB)')
            conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS '
                         'addok_key_idx ON addok (key)')

    def fetch(self, *keys):
        if not keys:  # Avoid invalid SQL.
            return
        keys = [key.decode() for key in keys]
        # SQLite requires to pass the same number of question marks.
        params = ','.join(['?'] * len(keys))
        query = 'SELECT key, data FROM addok WHERE key IN ({})'.format(params)
        with self.conn as conn:
            cursor = conn.execute(query, keys)
            for key, data in cursor.fetchall():
                yield key.encode(), data

    def upsert(self, *docs):
        self.lock.acquire()
        with self.conn as conn:
            conn.executemany('INSERT OR REPLACE INTO addok '
                             '(key, data) VALUES (?,?)', docs)
        self.lock.release()

    def remove(self, *keys):
        self.lock.acquire()
        with self.conn as conn:
            conn.executemany('DELETE FROM addok WHERE key=?', (keys, ))
        self.lock.release()

    def flushdb(self):
        os.unlink(config.SQLITE_DB_PATH)
        self.init()


def preconfigure(config):
    config.DOCUMENT_STORE_PYPATH = 'addok_sqlite_store.SQLiteStore'
    config.SQLITE_DB_PATH = 'addok.db'
