import psycopg2
# dbase for bot for using databases
# fix to run on postgresql table bot_users for users and bot_users_msg for messages
def safety_connection(func):
    def inner(*args, **kwargs):
        with psycopg2.connect(dbname='fn1131_2021', user='student', password='bmstu', host='195.19.32.74',port='5432') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res
    return inner

@safety_connection
def insert_user_into_table(conn, chat_id:str, name: str):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bot_users WHERE chat_id = '{chat_id}'".
                   format(chat_id=chat_id))
    count = cursor.fetchone()[0]
    conn.commit()
    if not count:
        cursor.execute("insert into bot_users (chat_id, name) values ('{chat_id}', '{name}')".format(chat_id=chat_id, name=name))
        print(f"Inserted users {chat_id} - {name} into db")
    else:
        print("This user is already in our psql db")
    cursor.close()

@safety_connection
def update_name_by_chat_id(conn, chat_id: str, name: str):
    cursor = conn.cursor()
    cursor.execute("select count(*) from bot_users where chat_id='{chat_id}'".format(chat_id=chat_id))
    count = cursor.fetchone()[0]
    conn.commit()
    if count:
        cursor.execute("update bot_users set name='{name}' where chat_id='{chat_id}'".format(name=name, chat_id=chat_id))
    else:
        return 'none'
    cursor.close()
    return 'replaced'

@safety_connection
def get_chat_id_by_name(conn, name: str):
    cursor = conn.cursor()
    cursor.execute("select chat_id from bot_users where name='{name}'".format(name=name))
    res = cursor.fetchall()
    conn.commit()
    cursor.close()
    if len(res) == 0:
        return None
    else:
        return res

@safety_connection
def chat_id_is_exist(conn, chat_id: str):
    cursor = conn.cursor()
    cursor.execute("select name from bot_users where chat_id='{chat_id}'".format(chat_id=chat_id))
    return len(cursor.fetchall()) != 0

@safety_connection
def name_is_exist(conn, name: str):
    cursor = conn.cursor()
    cursor.execute("select name from bot_users where name='{name}'".format(name=name))
    res = cursor.fetchall()
    return len(res) != 0

@safety_connection
def unsubscribe(conn, chat_id):
    cursor = conn.cursor()
    cursor.execute("delete from bot_users where chat_id='{chat_id}'".format(chat_id=chat_id))
    conn.commit()
    cursor.close()

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

@safety_connection
def get_all_user_name(conn):
    cursor = conn.cursor()
    cursor.execute("select name from bot_users")
    res = cursor.fetchall()
    conn.commit()
    cursor.close()
    if len(res) == 0:
        return None
    else:
        names = []
        for n in res:
            names.append(n[0])
        return names

@safety_connection
def get_name_by_chat_id(conn, chat_id: str):
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM bot_users WHERE chat_id = '{chat_id}'".format(chat_id=chat_id))
    res = cursor.fetchall()
    if(len(res) == 0):
        return "None"
    name = str(res[0])[2:-3]
    conn.commit()
    cursor.close()
    return name

@safety_connection
def get_info(conn):
    cursor = conn.cursor()
    cursor.execute("select * from bot_users")
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    info = ''
    for row in rows:
        info += 'name in db: ' + str(row[0]) + ' ; id: ' + str(row[1]) + '\n'
    return info

@safety_connection
def drop(conn):
    cursor = conn.cursor()
    cursor.execute("drop table bot_users")
    conn.commit()
    cursor.close()
