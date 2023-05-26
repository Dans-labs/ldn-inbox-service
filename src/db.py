import sqlite3
from sqlite3 import Error


def create_sqlite3_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_inbox_record(conn, inbox_rec):
    """
    Create a new project into the projects table
    :param conn:
    :param inbox_rec:
    :return: project id
    """
    sql = ''' INSERT INTO inbox(id, created_time, updated_time, sender, payload, payload_turtle)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, inbox_rec)
    conn.commit()
    return {"row-id": str(cur.lastrowid), "rec-id": str(inbox_rec[0])}


def select_all_inboxes(db_file):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, created_time, sender, payload, payload_turtle FROM inbox;")
        data = cursor.fetchall()
        print(data)
        return data  # CREATE JSON


def select_inbox_by_id(db_file, id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    sql = f"SELECT id, created_time, sender, payload, payload_turtle FROM inbox WHERE id='{id}';"

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        return data


def select_inbox_by_id(db_file, id):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    sql = f"SELECT id, created_time, sender, payload, payload_turtle FROM inbox WHERE id='{id}';"

    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)

        return data

#https://www.beekeeperstudio.io/blog/sqlite-json-with-text
def select_inbox(db_file):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    #TODO: Use json functionality - https://www.sqlite.org/json1.html
    # sql = f"SELECT inbox.id FROM inbox WHERE payload like '%\"target\":%https://archivalbot.data-stations.nl%';"
    sql = f"SELECT json_extract(payload, '$.target.id') FROM inbox;"
   # sql = f"SELECT id FROM inbox WHERE json_extract(payload, '$.target.id') LIKE '%https://archivalbot.data-stations.nl%';"
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)

        return data


def select_inbox_by_target_and_updated(db_file, target, updated_time):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    # TODO: Use json functionality - https://www.sqlite.org/json1.html
    # TODO: updated_time!!!
    sql = f"SELECT id, payload FROM inbox WHERE json_extract(payload, '$.target.id') LIKE '%{target}%';"
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

        print(data)

        return [dict(ix) for ix in data]

def select_inbox_by_updated_time(db_file, updated_time):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    # TODO: Use json functionality - https://www.sqlite.org/json1.html
    # TODO: updated_time!!!
    sql = f"SELECT id, payload FROM inbox WHERE json_extract(payload, '$.object.type') LIKE '%sorg:AboutPage%';"
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

        print(data)

        return [dict(ix) for ix in data]