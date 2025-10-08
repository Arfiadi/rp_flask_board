import psycopg2
from flask import current_app, g

def get_pg_db_conn():
    if 'db' not in g:
        # Menggunakan 'psql-db' sesuai hostname di docker-compose.yml
        g.db = psycopg2.connect(
            host="psql-db",
            database="flask_db",
            user="admin",
            password="P4ssw0rd"
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
