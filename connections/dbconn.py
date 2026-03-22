from pypika import NULL, Schema
from pypika import PostgreSQLQuery as Q
from pypika import Table, Field, Tuple
from pypika import Case, functions as fn
from fastapi import HTTPException
from psycopg2 import pool
from contextlib import contextmanager
import os 
from urllib.parse import urlparse

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql://neondb_owner:npg_3mj0RgQwEKiV@ep-proud-grass-alb5i6lj-pooler.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

data= urlparse(DATABASE_URL)
DB_HOST = data.hostname
DB_PORT = data.port or 5432
DB_NAME = data.path[1:]
DB_USER = data.username
DB_PASSWORD = data.password

pg_pool = pool.ThreadedConnectionPool(
    1, 20, 
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME)

@contextmanager
def connection():
    try:
        con = pg_pool.getconn()
        cur = con.cursor()
        yield cur
        con.commit()
    except Exception as e:
        con.rollback()
        cur.close()
        print("db error: {}".format(e))
        raise HTTPException(status_code=409, detail=str(e))
    finally:
        cur.close()
        pg_pool.putconn(con)



