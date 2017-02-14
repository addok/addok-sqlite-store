import sqlite3

from addok.config import config


class SQLiteStore:

    def __init__(self, *args, **kwargs):
        self.conn = sqlite3.connect(config.SQLITE_DB_PATH)
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

    def add(self, *docs):
        with self.conn as conn:
            conn.executemany('INSERT OR IGNORE INTO addok '
                             '(key, data) VALUES (?,?)', docs)

    def remove(self, *keys):
        with self.conn as conn:
            conn.executemany('DELETE FROM addok WHERE key=?', (keys, ))


def preconfigure(config):
    config.DOCUMENT_STORE_PYPATH = 'addok_sqlite.plugin.SQLiteStore'
    config.SQLITE_DB_PATH = 'addok.db'
