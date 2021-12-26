import psycopg2

# dbase for AUTOMATICALLY sending messages using messages databases
# fix to run on postgresql table bot_users for users and bot_users_msg for messages
def safety_connection(func):
    def inner(*args, **kwargs):
        with psycopg2.connect(dbname='fn1131_2021', user='student', password='bmstu', host='195.19.32.74',port='5432') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res
    return inner

@safety_connection
def update_state_messages(conn):
    cursor = conn.cursor()
    cursor.execute("update bot_users_msg set state='sent' where state='queued'")
    conn.commit()
    cursor.close()
    return "success"

@safety_connection
def get_queued_messages(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bot_users_msg WHERE state = 'queued'")
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    return rows




