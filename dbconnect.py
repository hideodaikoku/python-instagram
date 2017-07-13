import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "Printroom2020",
                           db = "pythonprogramming")
    c = conn.cursor()

    return c, conn
# import os
    # UPLOAD_FOLDER/filename
    # with open (os.path.test.jpg") as var
    # os,patg,hiub subdir r 