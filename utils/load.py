"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

File description:
Loading data
"""

import sqlite3
from utils.connect import connectDB
from utils.encryption import encMess


def loadMaster(username, password, website, refname):
    """
    This function will load all the encypted passwords 
    and details into the SQLite3 Database.
    """

    conn, curr = connectDB()

    # Encrypting the data before inserting into database

    encUsername =   encMess(username)
    encPassword =   encMess(password)
    encWebsite  =   encMess(website)
    encRefname  =   encMess(refname)

    insertData  =   (encRefname, encWebsite, encUsername, encPassword,) # Tuple of data to be inserted

    # SQL query to insert the encrypted data into the masterData table

    SQL_INSERT_DATA_QUERY = """
    INSERT INTO masterData (
        refname, website, username, passw
    ) VALUES (
        ?, ?, ?, ?
    );
    """

    try:
        curr.execute(SQL_INSERT_DATA_QUERY, insertData)
        conn.commit()
        return True
    except sqlite3.Error as erMessage:
        print("Command skipped. Error : ", erMessage)
        return False