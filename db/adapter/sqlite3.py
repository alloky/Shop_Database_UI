import sqlite3

from db.exception import *


class Sqlite3:
    """
    docstring for sqlite3Adapter

    now this class is signature influenced in cause of add_row(...) function.

    """

    def __init__(self, path_to_db, id_column_name, reserved_column_name,
                 decrease_column_name):
        self._path = path_to_db
        self._id_column_name = id_column_name
        self._reserved_column_name = reserved_column_name
        self._decrease_column_name = decrease_column_name

    def connect(self):
        self.sqlite_connection = sqlite3.connect(self._path)
        self.sqlite_cursor = self.sqlite_connection.cursor()
        self.sqlite_cursor.execute("PRAGMA foreign_keys = ON")

    def add_row(self, table_name="", row_sig="", row_array=list()):
        try:
            self.sqlite_cursor.execute("INSERT INTO {} ({}) VALUES ({})"
                                       .format(table_name, row_sig,
                                               ("?, " * len(row_array))[:-2]),
                                       tuple(row_array)
                                       )
            self.sqlite_connection.commit()
            return self.sqlite_cursor.lastrowid
        except Exception as e:
            arr = e.args[0].split()
            if (arr[0] == "no") and (arr[2] == "table"):
                raise DbException(e.args[0], DbErrorType.NO_SUCH_TABLE)
            if arr[0] == 'UNIQUE':
                raise ConstraintException(
                    e.args[0], (arr[-1].split('.'))[-1],
                    ConstraintErrorType.NOT_UNIQUE)
            elif arr[0] == 'CHECK':
                _e = ConstraintException(
                    e.args[0], (arr[-1].split('_'))[-2],
                    ConstraintErrorType.NOT_UNIQUE)
                sub_arr = arr[-1].split('_')
                if sub_arr[2] == "len":
                    _e.set_type(ConstraintErrorType.TOO_LONG)
                elif sub_arr[2] == "cor":
                    _e.set_type(ConstraintErrorType.INCORRECT_VALUE)
                raise _e
            else:
                raise DbException(e.args[0], DbErrorType.UNDEFINED_ERROR)

    def delete(self, table_name="", id_array=list()):
        try:
            self.sqlite_cursor.execute("DELETE FROM {} WHERE {} IN ({})"
                                       .format(table_name,
                                               self._id_column_name,
                                               str(id_array)[1:-1]))
            self.sqlite_connection.commit()
        except Exception as e:
            arr = e.args[0].split()
            if (arr[0] == "no") and (arr[2] == "table"):
                raise DbException(e.args[0], DbErrorType.NO_SUCH_TABLE)
            else:
                raise e

    def decrease(self, table_name="", pair_array=list()):
        try:
            for pair in pair_array:
                self.sqlite_cursor.execute(
                    "UPDATE {} SET {} = {} - {} WHERE {} = {}".format(
                        table_name,
                        self._decrease_column_name,
                        self._decrease_column_name,
                        pair[1],
                        self._id_column_name,
                        pair[0]
                    ))
            self.sqlite_connection.commit()
        except Exception as e:
            arr = e.args[0].split()
            if (arr[0] == "no") and (arr[2] == "table"):
                raise DbException(e.args[0], DbErrorType.NO_SUCH_TABLE)
            else:
                raise DbException(e)

    def reserve(self, table_name="", pair_array=list()):
        try:
            for pair in pair_array:
                self.sqlite_cursor.execute(
                    "UPDATE {} SET {} = {} + {} WHERE {} = {}".format(
                        table_name,
                        self._reserved_column_name,
                        self._reserved_column_name,
                        pair[1],
                        self._id_column_name,
                        pair[0]
                    ))
            self.sqlite_connection.commit()
        except Exception as e:
            arr = e.args[0].split()
            if (arr[0] == "no") and (arr[2] == "table"):
                raise DbException(e.args[0], DbErrorType.NO_SUCH_TABLE)
            if arr[0] == 'UNIQUE':
                raise ConstraintException(
                    e.args[0], (arr[-1].split('.'))[-1],
                    ConstraintErrorType.NOT_UNIQUE)
            elif arr[0] == 'CHECK':
                _e = ConstraintException(
                    e.args[0], (arr[-1].split('_'))[-2],
                    ConstraintErrorType.NOT_UNIQUE)
                sub_arr = arr[-1].split('_')
                if sub_arr[2] == "len":
                    _e.set_type(ConstraintErrorType.TOO_LONG)
                elif sub_arr[2] == "cor":
                    _e.set_type(ConstraintErrorType.INCORRECT_VALUE)
                raise _e
            else:
                raise e

    def unreserve(self, table_name="", pair_array=list()):
        try:
            for pair in pair_array:
                self.sqlite_cursor.execute(
                    "UPDATE {} SET {} = {} - {} WHERE {} = {}".format(
                        table_name,
                        self._reserved_column_name,
                        self._reserved_column_name,
                        pair[1],
                        self._id_column_name,
                        pair[0]
                    ))
            self.sqlite_connection.commit()
        except Exception as e:
            arr = e.args[0].split()
            if (arr[0] == "no") and (arr[2] == "table"):
                raise DbException(e.args[0], DbErrorType.NO_SUCH_TABLE)
            if arr[0] == 'UNIQUE':
                raise ConstraintException(
                    e.args[0], (arr[-1].split('.'))[-1],
                    ConstraintErrorType.NOT_UNIQUE)
            elif arr[0] == 'CHECK':
                _e = ConstraintException(
                    e.args[0], (arr[-1].split('_'))[-2],
                    ConstraintErrorType.NOT_UNIQUE)
                sub_arr = arr[-1].split('_')
                if sub_arr[2] == "len":
                    _e.set_type(ConstraintErrorType.TOO_LONG)
                elif sub_arr[2] == "cor":
                    _e.set_type(ConstraintErrorType.INCORRECT_VALUE)
                raise _e
            else:
                raise e

    def update(self, table_name, column_name, id, value):
        try:
            self.sqlite_cursor.execute(
                "UPDATE {} SET {} = ? WHERE {} = {}".format(
                    table_name,
                    column_name,
                    self._id_column_name,
                    id
                ), tuple([value]))
            self.sqlite_connection.commit()
        except Exception as e:
            arr = e.args[0].split()
            if (arr[0] == "no") and (arr[2] == "table"):
                raise DbException(e.args[0], DbErrorType.NO_SUCH_TABLE)
            if arr[0] == 'UNIQUE':
                raise ConstraintException(
                    e.args[0], (arr[-1].split('.'))[-1],
                    ConstraintErrorType.NOT_UNIQUE)
            elif arr[0] == 'CHECK':
                _e = ConstraintException(
                    e.args[0], (arr[-1].split('_'))[-2],
                    ConstraintErrorType.NOT_UNIQUE)
                sub_arr = arr[-1].split('_')
                if sub_arr[2] == "len":
                    _e.set_type(ConstraintErrorType.TOO_LONG)
                elif sub_arr[2] == "cor":
                    _e.set_type(ConstraintErrorType.INCORRECT_VALUE)
                raise _e
            else:
                raise e

    def commit(self):
        self.sqlite_connection.commit()

    def select_all(self, table_name=""):
        try:
            yield from self.sqlite_cursor.execute("SELECT * FROM {}"
                                                  .format(table_name))
        except Exception as e:
            arr = e.args[0].split()
            if (arr[0] == "no") and (arr[2] == "table"):
                raise DbException(e.args[0], DbErrorType.NO_SUCH_TABLE)
            else:
                raise DbException(e.args[0], DbErrorType.UNDEFINED_ERROR)

    def select_by_id(self, table_name="", id_array=list()):
        yield from self.sqlite_cursor.execute(
            "SELECT * FROM {} WHERE {} IN ({})".format(
                table_name,
                self._id_column_name,
                str(id_array)[1:-1]))

    def close_connection(self):
        self.sqlite_connection.close()

    def create_tables(self):
        qry = open('db/adapter/scripts/sqlite/create.sql', 'r').read()
        self.sqlite_cursor.executescript(qry)
        self.sqlite_connection.commit()

    def execute(self, exec_str):
        self.sqlite_cursor.execute(exec_str)

    def get_all_tables(self):
        yield self.sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
