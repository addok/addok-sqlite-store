# addok-sqlite-store

Addok plugin to store documents in SQLite instead of Redis to reduce memory usage.

## Features

- **SQLite storage**: Store documents in a SQLite database instead of Redis
- **Memory optimization**: Reduce Redis RAM usage for large datasets

## Installation

```bash
pip install addok-sqlite-store
```

## Configuration

Add the following to your Addok configuration file to activate the plugin:

```python
# Use SQLite as document store
DOCUMENT_STORE_PYPATH = 'addok_sqlite_store.SQLiteStore'
```

The SQLite database will be created at `addok.db` by default. You can customize the path:

```python
# Optional: customize the database path
SQLITE_DB_PATH = '/path/to/your/database.db'
```

Or use environment variables:

```bash
export ADDOK_DOCUMENT_STORE_PYPATH='addok_sqlite_store.SQLiteStore'
export ADDOK_SQLITE_DB_PATH='/path/to/your/database.db'  # optional
```
