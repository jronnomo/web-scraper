import sqlite3

# Establish connection
connection = sqlite3.connect('data-example.db')
cursor = connection.cursor()

# Query data with condition
cursor.execute("SELECT band, date FROM events WHERE date='2088.10.15'")
rows = cursor.fetchall()
print(rows)


# Insert new row
# cursor.execute("INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14')")


# Insert many new rows
new_rows = [('Cats', 'Cats City', '2088.10.17'),
            ('Dogs', 'Dogs City', '2088.10.17')]

cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()
