import marshal
import sqlite3

from addok.config import config


class DocumentStorage:

    def __init__(self, *args, **kwargs):
        self.conn = sqlite3.connect(config.SQLITE_DB_PATH)
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS doc (key VARCHAR, data BLOB)')
        cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS '
                    'doc_key_idx ON doc (key)')
        self.conn.commit()
        cur.close()

    def get(self, *keys):
        cur = self.conn.cursor()
        for key in keys:
            cur.execute('SELECT data FROM doc WHERE key=?', (key.decode(),))
            self.conn.commit()
            row = cur.fetchone()
            yield marshal.loads(row[0])
        cur.close()

    def add(self, *docs):
        cur = self.conn.cursor()
        data = [(k, marshal.dumps(d)) for k, d in docs]
        cur.executemany('INSERT OR IGNORE INTO doc '
                        '(key, data) VALUES (?,?)', data)
        self.conn.commit()
        cur.close()
        for key, doc in docs:
            yield doc

    def remove(self, *docs):
        cur = self.conn.cursor()
        keys = [k for k, d in docs]
        cur.executemany('DELETE FROM doc WHERE key=?', keys)
        self.conn.commit()
        cur.close()
        for key, doc in docs:
            yield doc


def preconfigure(config):
    config.DOCUMENT_STORAGE = 'addok_sqlite.plugin.DocumentStorage'
    config.SQLITE_DB_PATH = 'addok.db'
    config.STORAGE_IMPORT_CHUNK_SIZE = 10000
