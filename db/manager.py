class DbManager:
	"""Db managment class"""

	def __init__(self, adapter):
		self.adapter = adapter
		self.adapter.connect()

	def __str__(self):
		return "This is dbManager with " + self.adapter 

	def add_row(self, tableName="", rowArray=[]):
		if not rowArray or not tableName:
			return
		self.adapter.add_row(tableName, rowArray)

	def delete(self, tableName="", idArray=[]):
		if not idArray:
			return
		self.adapter.delete(tableName, idArray)

	def reserve(self, idArray=[]):
		if not idArray:
			return
		self.adapter.reserve(idArray)

	def decrease(self, idArray=[]):
		if not idArray:
			return
		self.adapter.decrease(idArray)

	def update(self, id, rowArray=[]):
		if not rowArray or (id < 0):
			return
		self.adapter.update(id, rowArray)

	def commit(self):
		self.adapter.commit()

	def select_all(self, tableName=""):
		if not tableName:
			return
		yield from self.adapter.select_all(tableName)
