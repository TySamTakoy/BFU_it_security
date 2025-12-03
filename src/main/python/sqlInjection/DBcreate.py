import sqlite3
import os

dbname = 'users.db'

try:
    os.remove(dbname)
except:
    pass

con = sqlite3.connect(dbname)
cur = con.cursor()

cur.execute('CREATE TABLE users(username, password, secret_number)')
cur.execute("""
    INSERT INTO users VALUES 
        ('vova', '1234', 225),
        ('masha', 'qwerty', 1337),
        ('petya', 'abcd', 42),
        ('muhhamed','muhhamed', 1000000)
""")

con.commit()
