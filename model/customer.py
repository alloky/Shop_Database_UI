class Customer:
    def __init__(self, from_db):
        self.id = from_db[0]
        self.surname = from_db[1]
        self.name = from_db[2]
        self.phone = from_db[3]
        self.address = from_db[4]

    @classmethod
    def add(cls, data):
        return Customer([None, *data])

    def get_initials(self):
        return '{} {}.'.format(self.surname, self.name[0])

    def get_full_name(self):
        return '{} {}.'.format(self.surname, self.name)
