from gateway import utility



def create_bug(name, description, priority):
    """"""
    db_conn, db_cursor = utility.open_database()

    statement = ("INSERT INTO bugs "
                 "(bugName, description, priority) "
                 "VALUES (%s, %s, %s)")
    db_cursor.execute(statement, (name, description, priority))
    db_conn.commit()

    bugID = db_cursor.lastrowid

    utility.close_database(db_conn, db_cursor)
    return bugID

def get_bugs():
    db_conn, db_cursor = utility.open_database()
    bugs = []

    # MySql statement to get everything from a table
    statement = ("SELECT * FROM bugs")
    db_cursor.execute(statement)

    for bug in db_cursor:
        bugs.append(bug)

    utility.close_database(db_conn, db_cursor)

    return bugs

def get_a_bug(id):
    """
    Delete a single bug using the given bug id
    :param id: The ID of the bug given from the user
    :return: the information on the specific bug
    """
    db_conn, db_cursor = utility.open_database()

    statement = ("SELECT * FROM bugs "
                 "WHERE id=%s")
    db_cursor.execute(statement, (id,))     # For some reason the tuple has to have an empty second element if
                                            # only one parameter is given.

    for item in db_cursor:
        bug = item

    utility.close_database(db_conn, db_cursor)

    return bug

def delete_a_bug(id):
    """
    Delete a single bug using the given bug id
    :param id: The ID of the bug given from the user
    :return: the id of the deleted bug
    """
    db_conn, db_cursor = utility.open_database()

    statement = ("DELETE FROM bugs "
                 "WHERE id=%s")
    db_cursor.execute(statement, (id,))     # For some reason the tuple has to have an empty second element if
                                            # only one parameter is given.
    bugID = db_cursor.rowcount             # This is the best way to get the item that I know of.

    db_conn.commit()

    utility.close_database(db_conn, db_cursor)

    return bugID

def update_bug(name, description, priority, id):
    """
    Delete a single property using the given property id
    :param id: The ID of the property given from the user
    :return: the information on the specific property
    """
    db_conn, db_cursor = utility.open_database()

    statement = ("UPDATE bugs "
                 "SET bugName=%s, "
                 "description=%s, "
                 "priority=%s "
                 "WHERE id=%s")
    db_cursor.execute(statement, (name, description, priority, id))

    bug_id = db_cursor.rowcount

    db_conn.commit()
    utility.close_database(db_conn, db_cursor)

    return bug_id