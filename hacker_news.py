import os
import time
import calendar
from sqlite3 import dbapi2 as sq3


def get_db(dbfile):
    sqlite_db = sq3.connect(os.path.join(".", dbfile))
    return sqlite_db

def init_db(dbfile, schema):
    """Creates the database tables."""
    db = get_db(dbfile)
    db.cursor().executescript(schema)
    db.commit()
    return db

def get_last_ts(db):
    cursor = db.cursor().execute('SELECT MAX(created_at) FROM hn_submissions;')
    result = cursor.fetchone()
    try:
        return calendar.timegm(time.strptime(result[0] + ' UTC', '%Y-%m-%d %H:%M:%S %Z'))
    except Exception:
        return calendar.timegm((1990,1,1,0,0,0,))
