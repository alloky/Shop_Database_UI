class Order:
    def __init__(self):
        self._cart = dict()
        self._customer = None

    def to_cart(self, products):
        for p in products:
            if p.id in self._cart:
                self._cart[p.id].count += 1
            else:
                p.count = 1
                self._cart[p.id] = p

    def set_customer(self, customer):
        self._customer = customer

    def get_cart(self):
        return list(self._cart.values())

    def remove_from_cart(self, products):
        for prod in products:
            self._cart.pop(prod.id, None)

    def get_initials(self):
        return self._customer.get_initials()

    def get_customer(self):
        return self._customer

    def get_sum(self):
        return sum([x.price * x.count for x in self.get_cart()])
