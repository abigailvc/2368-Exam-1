# MySQL connection helper for Exam 1 - Troop API
# Adapted from Homework 2 (Zoo API)

import mysql.connector
from mysql.connector import Error

def create_connection(hostname, uname, passwd, dbname):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=hostname,
            user=uname,
            password=passwd,
            database=dbname
        )
        return conn
    except Error as e:
        print("Connection error:", e)
        return None
