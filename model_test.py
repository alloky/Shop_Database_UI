import model
from db import exception

shop = model.Shop()

try:
    shop.create_db("data/model_test.db", model.DbType.SQLITE)
except Exception as e:
    print(e, e.args, vars(e))
    shop.open_db("data/model_test.db", model.DbType.SQLITE)

products = [[1, "cookie", 42, 1, 0],
            [2, "milk", 15, 2, 0],
            [3, "potatoes", 11, 3, 0],
            [4, "vodka", 11, 4, 0]
            ]

prodP = []

for i in ['deals','products','customers']:
    print(tuple([i]) in list(shop.database.adapter.sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")))

for prod in products:
    try:
        shop.add_product(model.Product(prod))
    except exception.ConstraintException as e:
        print(e.column_name, e.typeNum)
    prodP.append(model.Product(prod))



customer = model.Customer([0,
                           "Pupkin",
                           "Vasya",
                           "8-800-555-35-35",
                           "NY, Wall Stret 17, 32 floor"])

shop.add_customer(customer)


print("=================Customers===============")

print(list(shop.get_from("customers")))

shop.order.set_customer(customer)

print(list(shop.get_from("product")))


for p in prodP:
    p.count = 1

shop.to_cart(prodP)

print("Sum :{}".format(shop.order.get_sum()))

print(shop.order.get_customer().get_initials())

print("=================Products================")

print(list(shop.get_from("products")))

shop.remove_from_cart([prodP[3]])

print("Sum :{}".format(shop.order.get_sum()))

print("============Products {removed last}=======")

print(list(shop.get_from("products")))

shop.place_order()

shop.clear_order()


# print(shop.get_order())

# shop.to_cart([1, 2, 3])

# print(shop.get_order())

# shop.remove_from_cart([2])

# print(shop.get_order())

# shop.to_cart([4])

# print(shop.get_order())

# shop.remove_from_cart([1, 2])


print("=================Customers===============")

print(list(shop.get_from("customers")))

print("=================Products================")

print(list(shop.get_from("products")))
