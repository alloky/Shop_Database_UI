from dbmanager import dbManager
from dbmanager import sqlite3Adapter

sql3Adpt = sqlite3Adapter.sqlite3Adapter("db/test.db", "id") 
db = dbManager.dbManager(sql3Adpt)
	

# Create table
sql3Adpt.sqliteCursor.execute('''CREATE TABLE stocks
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,name varchar(100), count INT, price INT, reserved INT DEFAULT 0)''')

sql3Adpt.sqliteCursor.execute("CREATE UNIQUE INDEX stoks_ind ON stocks (id)")

# Insert a row of data
db.add_row("stocks",["product", 3, 100])
db.add_row("stocks",["product", 3, 100])
db.add_row("stocks",["product", 3, 100])
db.add_row("stocks",["product", 3, 100])

# Save (commit) the changes
#db.commit()

print("================Nothing deleted======================")

for row in db.select_all("stocks"):
	print(row)


db.delete("stocks", [1,4])


print("================{1,4} deleted======================")


for row in db.select_all("stocks"):
	print(row)

db.delete("stocks", [2,3] )

sql3Adpt.sqliteCursor.execute("DROP TABLE stocks")

sql3Adpt.sqliteConnection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
sql3Adpt.sqliteConnection.close()