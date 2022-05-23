"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

File description:
Database connection 
"""

import os
import sqlite3

def connectDB():
    """
    Establishes connection with the database and initializes
    the master table in database.
    """

    conn = sqlite3.connect("masterData.db") # Connection with the database
    curr = conn.cursor()                    # Setting up the cursor for connection


    # SQL Query to create the master table in the database.
    # The table will consist of 5 columns : 
    #   1. ID       :   Record ID.
    #   2. refname  :   Stores the unique discord ID of every user.
    #   3. website  :   Stores the website entered by user.
    #   4. username :   Stores the username entered by user for the website.
    #   5. passw    :   Stores the password for website entered by user.
    #
    # All columns are assigned 'blob' data type to store the encrypted data.


    SQL_CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS masterData (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        refname     BLOB,
        website     BLOB,
        username    BLOB,
        passw       BLOB
    );
    """

    try:
        curr.execute(SQL_CREATE_TABLE_QUERY) 
        conn.commit()
    except sqlite3.Error as erMessage:
        print("Command skipped. Error : ", erMessage)

    return conn, curr