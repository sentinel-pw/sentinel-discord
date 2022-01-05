"""
Copyright © Raveesh Yadav 2021 - htts://github.com/Raveesh1505

File description:
Loading data
"""

import csv

def loadMaster(username, password, website, refname):
    """
    This function will load all the encypted passwords 
    and details into the csv file.
    """

    with open ("masterData.csv", mode='a') as masterFile:
        writer = csv.writer(masterFile, delimiter=",", quotechar = '"')
        writer.writerow([refname, username, password, website])
    masterFile.close()
    return True