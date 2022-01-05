"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

File description:
Password print
"""

import csv
import utils.encryption as encryption
from table2ascii import table2ascii as t2a, PresetStyle

def releasePass(refname):
    """
    This function will show all the registered passwords 
    of the user in the database.
    """

    passList = []   # Innitialising and empty array

    encryption.decFile("utils/masterData.csv")

    with open ("utils/masterData.csv") as passFile:
        reader = csv.reader(passFile, delimiter=',')
        line_count = 0
        for row in reader:
            if (line_count != 0):
                if (row[0]) == refname:
                    element = row
                    passList.append(element)
            line_count += 1
    
    encryption.encFile("utils/masterData.csv")

    output = t2a(
        header = ["User", "Username", "Password", "Website"],
        body = passList,
        first_col_heading = True,
        style = PresetStyle.thin_rounded,
    )

    return output