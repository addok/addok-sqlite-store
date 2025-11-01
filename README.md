# addok-sqlite-store

Addok plugin to store documents in SQLite instead of Redis to reduce memory usage.

## Features

- **SQLite storage**: Store documents in a SQLite database instead of Redis
- **Memory optimization**: Reduce Redis RAM usage for large datasets
- **Automatic registration**: Plugin registers itself when installed

## Installation

```bash
pip install addok-sqlite-store
```

## Configuration

The plugin will register itself when installed, by setting the correct
`DOCUMENT_STORE_PYPATH`.

Define the path where the SQLite database will be created:

```python
SQLITE_DB_PATH = "/path/to/your/database.db"
```
