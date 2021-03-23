import sqlite3

con = sqlite3.connect('767db.db') # TODO what format will the data come in?
cur = con.cursor()
cur.execute('''CREATE TABLE tbl (name, topic, authors)''')

cur.execute("INSERT INTO tbl VALUES ('cats','climate change','sneha')")
cur.execute("INSERT INTO tbl VALUES ('dogs','climate change','sneha')")
cur.execute("INSERT INTO tbl VALUES ('raccoons','climate change','sneha')")
cur.execute("INSERT INTO tbl VALUES ('dogs','pink','sneha')")
cur.execute("INSERT INTO tbl VALUES ('dogCs','purple','sneha')")

for row in cur.execute('SELECT * FROM tbl'):
        print(row)

con.commit()
con.close()