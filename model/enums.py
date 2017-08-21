import enum


class DbType(enum.Enum):
    NOT_CHOSEN = enum.auto()
    SQLITE = enum.auto()
    POSTGRES = enum.auto()


class Action(enum.Enum):
    NOT_CHOSEN = enum.auto()
    CREATE = enum.auto()
    OPEN = enum.auto()
