class Product:
    def __init__(self, from_db=[None] * 5):
        self.id = from_db[0]
        self.name = from_db[1]
        self.count = from_db[2]
        self.price = from_db[3]
        self.reserved = from_db[4]

    @classmethod
    def add(cls, data):
        return cls([None, *data, None])

    def __str__(self):
        return "id: {}\nname: {}\ncount: {}\nprice: {}\nreserve: {}".format(
            self.id, self.name, self.count, self.price, self.reserved)
