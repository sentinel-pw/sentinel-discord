"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

File description:
Password print
"""

import sqlite3
from utils.encryption import decMess
from utils.connect import connectDB
from table2ascii import table2ascii as t2a, PresetStyle


def releasePass(refname):
    """
    This function will show all the registered passwords 
    of the user in the database.
    """
    conn, curr = connectDB()
    passList = []                   # Initializing and empty array

    SQL_EXTRACTION_QUERY = """
    SELECT * FROM masterData;
    """

    try:
        curr.execute(SQL_EXTRACTION_QUERY)
        fetchData = curr.fetchall()
        conn.commit()
    except sqlite3.Error as erMessage:
        print("Command Skipped. Error : ", erMessage)


    for i in range(len(fetchData)):
        if decMess(fetchData[i][1]) == refname:                                                         # Refering to the unique discord ID
            decTuple = (decMess(fetchData[i][3]), decMess(fetchData[i][4]), decMess(fetchData[i][2]))   # Tuple with decrypted data
            passList.append(decTuple)

    # Output on Discord
    output = t2a(
        header = ["Username", "Password", "Website"],
        body = passList,
        first_col_heading = True,
        style = PresetStyle.thin_rounded,
    )

    return output