import enum


class ConstraintErrorType(enum.Enum):
    INCORRECT_VALUE = enum.auto()
    TOO_LONG = enum.auto()
    NOT_UNIQUE = enum.auto()


class DbErrorType(enum.Enum):
    UNDEFINED_ERROR = enum.auto()
    ALREADY_EXISTS = enum.auto()
    NO_SUCH_TABLE = enum.auto()
    DB_NOT_CONNECTED = enum.auto()


class DbException(Exception):
    """Custom db exception, value information is stored in self.message"""

    def __init__(self, message, type_num=DbErrorType.UNDEFINED_ERROR):
        super(DbException, self).__init__(message)
        self.message = message
        self.type_num = type_num

    def set_type(self, type_num):
        self.type_num = type_num


class ConstraintException(Exception):
    """Custom db exception, value information is stored in self.message"""

    def __init__(self, message, column_name, type_num):
        super(ConstraintException, self).__init__(message)
        self.column_name = column_name
        self.type_num = type_num

    def set_type(self, type_num):
        self.type_num = type_num
