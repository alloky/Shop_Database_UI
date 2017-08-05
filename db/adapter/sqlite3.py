import sqlite3

class Sqlite3:
	"""docstring for sqlite3Adapter
		
		now this class is signature influenced in cause of add_row(...) function.

	"""
	_path = ""
	_idColumnName ="id"
	_insertFormat = "name, count, price"

	def __init__(self, pathToDb):
		self._path = pathToDb

	def connect(self):
		self.sqlite_connection = sqlite3.connect(self._path)
		self.sqlite_cursor = self.sqlite_connection.cursor()

	def add_row(self, tableName="", rowArray=[]):
		self.sqlite_cursor.execute("INSERT INTO {} ({}) VALUES ({})".format(tableName,self._insertFormat,str(rowArray)[1:-1]))

	def delete(self, tableName="", idArray=[]):
		self.sqlite_cursor.execute("DELETE FROM {} WHERE {} IN ({})".format(tableName,self._idColumnName,str(idArray)[1:-1]))

	def decrease(self, idArray=[]):
		if not idArray:
			return
		self.adapter.decrease(idArray)

	def reserve(self, idArray=[]):
		if not idArray:
			return
		self.adapter.reserve(idArray)

	def update(self, id, rowArray=[]):
		if not rowArray or (id < 0):
			return
		self.adapter.update(id, rowArray)


	def commit(self):
		self.sqlite_connection.commit()

	def select_all(self, tableName=""):
		yield from self.sqlite_cursor.execute("SELECT * FROM {}".format(tableName))