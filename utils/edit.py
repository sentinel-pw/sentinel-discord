"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

File description:
Password print
"""

import csv
from table2ascii import table2ascii as t2a
import utils.encryption as encryption

def confirmData(refname, username, website):
    passList = []   # Innitialising and empty array

    encryption.decFile("utils/masterData.csv")

    with open ("utils/masterData.csv") as passFile:
        reader = csv.reader(passFile, delimiter=',')
        line_count = 0
        for row in reader:
            if (line_count != 0):
                if (row[0]) == refname and row[1] == username and row[3] == website:
                    element = row
                    passList.append(element)
            line_count += 1
    
    encryption.encFile("utils/masterData.csv")

    output = t2a(
        header = ["User", "Username", "Password", "Website"],
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

    encryption.decFile("utils/masterData.csv")
    
    lines = []  # Innitialising an empty list

    with open('utils/masterData.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if row[0] == refname and row[1] == username and row[3] == website:
                lines.remove(row)
    with open('utils/masterData.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    
    encryption.encFile("utils/masterData.csv")
    return True