class Column:
    def __init__(self, name, prop, description='', user_init=True,
                 max_length=30):
        self.name = name  # for db and class of each string
        self.display_name = None  # link to locale

        self.user_init = user_init
        self.proportion = prop  # for auto resize
        self.description = description  # approx type for db
        self.max_length = max_length


class Table:
    def __init__(self, name, source, row_class=None):
        self.name = name
        self.display_source = source
        self.row_class = row_class
        self.columns = list()

    def add_column(self, column):
        column.display_name = self.display_source[column.name]
        self.columns.append(column)


class Database:
    def __init__(self, name):
        self.name = name
        self.tables = dict()
        self.create_order = list()

    def add_table(self, table):
        self.create_order.append(table.name)
        self.tables[table.name] = table

    def __getitem__(self, item):
        return self.tables[item]
