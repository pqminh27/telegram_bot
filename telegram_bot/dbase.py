import sqlite3
import os
import psycopg2
import asyncio

def safety_connection(func):
    def inner(*args, **kwargs):
        with psycopg2.connect(dbname='fn1131_2021', user='student', password='bmstu', host='195.19.32.74',
                              port='5432') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res
    return inner

# @safety_connection
# def init_db(conn):
#     cursor = conn.cursor()
#     cursor.execute('CREATE TABLE IF NOT EXISTS dbb('
#                    'chat_id text NOT NULL, '
#                    'name text NOT NULL, state integer NOT NULL,'
#                    'PRIMARY KEY (user_id))')
#
#     conn.commit()

@safety_connection
def get_chat_id_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute("select chat_id from bot_users where name='{name}'".format(name=name))
    res = cursor.fetchall()
    # or fetchone() because name is unique in db bot_users
    conn.commit()
    cursor.close()
    if len(res) == 0:
        return None
    else:
        return res

@safety_connection
def drop(conn):
    cursor = conn.cursor()
    cursor.execute("drop table bot_users")
    conn.commit()
    cursor.close()


# get all chat_id that links with a bot
@safety_connection
def get_all_chat_id(conn):
    cursor = conn.cursor()
    cursor.execute("select chat_id from bot_users")
    rows = cursor.fetchall()
    conn.commit()
    if len(rows) == 0:
        return None
    cursor.close()
    res = []
    for row in rows:
        res.append(row[0])
    return res







