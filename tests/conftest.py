def pytest_configure():
    from addok import hooks
    import addok_sqlite_store
    from addok.config import config
    config.DOCUMENT_STORE_PYPATH = 'addok_sqlite_store.SQLiteStore'
    config.SQLITE_DB_PATH = 'addok_test.db'
    hooks.register(addok_sqlite_store)


def pytest_runtest_teardown():
    from addok.ds import DS
    DS.conn.execute('DELETE FROM addok')
