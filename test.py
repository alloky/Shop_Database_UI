import db
import db.adapter

sql3Adpt = db.adapter.Sqlite3("data/test.db")
database = db.DbManager(sql3Adpt)

# Create table
sql3Adpt.sqlite_cursor.execute('''CREATE TABLE stocks
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,name varchar(100), 
             count INT, price INT, reserved INT DEFAULT 0)''')

sql3Adpt.sqlite_cursor.execute("CREATE UNIQUE INDEX stoks_ind ON stocks (id)")

# Insert a row of data
database.add_row("stocks", ["product", 3, 100])
database.add_row("stocks", ["product", 3, 100])
database.add_row("stocks", ["product", 3, 100])
database.add_row("stocks", ["product", 3, 100])

# Save (commit) the changes
database.commit()

print("================Nothing deleted======================")

for row in database.select_all("stocks"):
    print(row)

database.delete("stocks", [1, 4])

print("================{1,4} deleted======================")

for row in database.select_all("stocks"):
    print(row)

database.delete("stocks", [2, 3])

sql3Adpt.sqlite_cursor.execute("DROP TABLE stocks")

sql3Adpt.sqlite_connection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
sql3Adpt.sqlite_connection.close()
