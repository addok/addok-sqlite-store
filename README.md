# Addok SQlite store plugin

Store your documents into a SQlite database to save Redis RAM usage.


## Install

    pip install addok-sqlite-store


## Configuration

The plugin will register itself when installed, by setting the correct
`DOCUMENT_STORE_PYPATH`.

You want to define the path where the SQLite database will be created, by
setting `SQLITE_DB_PATH` into your local
[configuration](http://addok.readthedocs.io/en/latest/config/).
