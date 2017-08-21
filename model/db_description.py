import db
from .product import Product
from .customer import Customer
from model.constants import constants as cnst
from gui.locale import rus as locale

products = db.Table('products', locale.PRODUCT_SOURCE, Product)
products.add_column(db.Column('id', 1, 'INTEGER PRIMARY KEY AUTOINCREMENT',
                              user_init=False))
products.add_column(db.Column('name', 4, 'VARCHAR(100) UNIQUE NUT NULL'))
products.add_column(db.Column('count', 2, 'INT NOT NULL CHECK (count >= 0)',
                              max_length=cnst.MAX_INT_LENGTH))
products.add_column(db.Column('price', 2, 'INT CHECK (price >= 0)',
                              max_length=cnst.MAX_INT_LENGTH))
products.add_column(db.Column('reserved', 3,
                              'INT DEFAULT 0 CHECK (reserved >= 0)',
                              user_init=False, max_length=cnst.MAX_INT_LENGTH))

customers = db.Table('customers', locale.CUSTOMER_SOURCE, Customer)
customers.add_column(db.Column('id', 1, 'INTEGER PRIMARY KEY AUTOINCREMENT',
                               user_init=False))
customers.add_column(db.Column('surname', 4, 'VARCHAR(100) NOT NULL'))
customers.add_column(db.Column('name', 4, 'VARCHAR(100) NOT NULL'))
customers.add_column(db.Column('phone', 3, 'VARCHAR(30)'))
customers.add_column(db.Column('address', 5, 'VARCHAR(200) NOT NULL',
                               max_length=cnst.MAX_ADDRESS_LENGTH))

deals = db.Table('deals', locale.DEALS_SOURCE)
deals.add_column(db.Column('id', 1, 'INTEGER PRIMARY KEY AUTOINCREMENT',
                           user_init=False))
deals.add_column(db.Column('customer_id', 2, 'INTEGER FOREIGN KEY customers'))
deals.add_column(db.Column('dttm', 3, 'timestamp', user_init=False))

storage = db.Database('storage')
storage.add_table(products)
storage.add_table(customers)
storage.add_table(deals)

order = db.Table('order', locale.PRODUCT_SOURCE)
order.add_column(db.Column('id', 1))
order.add_column(db.Column('name', 5))
order.add_column(db.Column('price', 2))
order.add_column(db.Column('count', 2))
