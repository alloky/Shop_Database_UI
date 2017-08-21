from .exception import DbException, DbErrorType


class Manager:
    """Db management class"""

    def __init__(self, adapter):
        self.adapter = adapter
        try:
            self.adapter.connect()
        except Exception as e:
            raise DbException(e.args[0])

    def __str__(self):
        return "This is DbManager with " + self.adapter

    def add_row(self, table_name="", row_sig="", row_array=list()):
        if not row_array or not table_name:
            return
        try:
            # autocommit inside
            rid = self.adapter.add_row(table_name, row_sig, row_array)
            return rid
        except DbException as e:
            raise e

    def delete(self, table_name="", id_array=list()):
        if not id_array:
            return
        try:
            self.adapter.delete(table_name, id_array)
            self.commit()
        except DbException as e:
            raise e

    def reserve(self, table_name="", pair_array=list()):
        if (not pair_array) or (not table_name):
            return
        try:
            self.adapter.reserve(table_name, pair_array)
            self.commit()
        except DbException as e:
            raise e
        except Exception as e:
            raise DbException(e.args[0])

    def unreserve(self, table_name="", pair_array=list()):
        if (not pair_array) or (not table_name):
            return
        try:
            self.adapter.unreserve(table_name, pair_array)
            self.commit()
        except DbException as e:
            raise e
        except Exception as e:
            raise DbException(e.args[0])

    def decrease(self, table_name="", pair_array=list()):
        if (not pair_array) or (not table_name):
            return
        try:
            self.adapter.decrease(table_name, pair_array)
            self.commit()
        except DbException as e:
            raise e
        except Exception as e:
            raise DbException(e.args[0])

    def update(self, table_name, column_name, id, value):
        if (id < 0) or not column_name:
            return
        try:
            self.adapter.update(table_name, column_name, id, value)
            self.commit()
        except DbException as e:
            raise e

    def commit(self):
        self.adapter.commit()

    def select_all(self, table_name=""):
        if not table_name:
            return
        try:
            yield from self.adapter.select_all(table_name)
        except DbException as e:
            raise e
        except Exception as e:
            raise DbException(e.args[0])

    def select_by_id(self, table_name="", id_array=list()):
        if not id_array:
            return []
        try:
            yield from self.adapter.select_by_id(table_name, id_array)
        except DbException as e:
            raise e
        except Exception as e:
            raise DbException(e.args[0])

    def close_connection(self):
        try:
            self.adapter.close_connection()
        except Exception as e:
            raise DbException(e.args[0])

    def create_tables(self):
        try:
            self.adapter.create_tables()
        except Exception as e:
            raise DbException(e.args[0], DbErrorType.ALREADY_EXISTS)

    def get_all_tables(self):
        try:
            yield self.adapter.get_all_tables()
        except Exception as e:
            raise DbException(e.args[0])
