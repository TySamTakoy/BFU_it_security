import sqlite3

dbname='users.db'

username = input('Enter username:')
password = input('Enter password:')

con = sqlite3.connect(dbname)
cur = con.cursor()

res=cur.execute(f"SELECT username FROM users WHERE username='{username}' AND password='{password}'")
r=res.fetchone()
#print(r)

if r != None:
    print(f'Welcome {username}!')
    res = cur.execute(f"SELECT secret_number FROM users WHERE username='{username}'")
    r = res.fetchone()
    print(f'Your secret number is {r[0]}')
else:
    print('Bad login or password')
