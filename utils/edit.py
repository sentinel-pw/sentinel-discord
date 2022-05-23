"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

File description:
Password print
"""

import sqlite3
from table2ascii import table2ascii as t2a
from utils.encryption import decMess
from utils.connect import connectDB


def confirmData(refname, username, website):
    """
    This function displays the requested passwords to the user.
    This function acts as a confirmatory function prior to performing
    the deletion of the requested password from the database.
    """

    conn, curr = connectDB()    # Establishing the connection with database
    passList = []               # Initializing and empty array

    SQL_SYNTAX_EXTRACT = """
    SELECT * FROM masterData;
    """

    try:
        curr.execute(SQL_SYNTAX_EXTRACT)
        fetchData = curr.fetchall()
        conn.commit()
    except sqlite3.Error as erMessage:
        print("Command Skipped. Error : ", erMessage)


    for i in range(len(fetchData)):
        if (decMess(fetchData[i][1]) == refname) and (decMess(fetchData[i][2]) == website) and (decMess(fetchData[i][3]) == username):
            decTuple = (decMess(fetchData[i][3]), decMess(fetchData[i][4]), decMess(fetchData[i][2]))   # Tuple with decrypted data
            passList.append(decTuple)

    # Discord output
    output = t2a(
        header = ["Username", "Password", "Website"],
        body = passList,
        first_col_heading = True,
    )

    return output


def deletePass(refname, username, website):
    """
    This function will delete a registered password
    of the user provided with username and webiste
    credentials.
    """

    conn, curr = connectDB()    # Establishing the connection with database

    # SQL Syntax to extract the data. Will be used to locate the data in table.
    SQL_SYNTAX_EXTRACT = """
    SELECT * FROM masterData;
    """

    # SQL Syntax to delete the data from table.
    SQL_SYNTAX_DELETE = """
    DELETE FROM masterData
    WHERE ID = ?
    ;
    """

    try:
        curr.execute(SQL_SYNTAX_EXTRACT)
        fetchData = curr.fetchall()
        conn.commit()
    except sqlite3.Error as erMessage:
        print("Command Skipped. Error : ", erMessage)

    
    for i in range(len(fetchData)):
        if (decMess(fetchData[i][1]) == refname) and (decMess(fetchData[i][2]) == website) and (decMess(fetchData[i][3]) == username):
            flag = i+1
    
    try:
        curr.execute(SQL_SYNTAX_DELETE, (flag,))
        conn.commit()
        return True
    except sqlite3.Error as erMessage:
        print("Command Skipped. Error : ", erMessage)
        return False