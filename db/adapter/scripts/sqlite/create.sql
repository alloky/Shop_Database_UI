CREATE TABLE IF NOT EXISTS products (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  name     TEXT,
  count    INT,
  price    INT CHECK (price >= 0),
  reserved INT                 DEFAULT 0,
  CONSTRAINT chk_name_unq UNIQUE (name),
  CONSTRAINT chk_name_len CHECK (name IS NOT NULL AND length(name) <= 50),
  CONSTRAINT chk_count_cor CHECK (count >= 0),
  CONSTRAINT chk_price_cor CHECK (price >= 0),
  CONSTRAINT chk_reserved_cor CHECK (reserved >= 0 AND reserved <= count)
);

CREATE TABLE IF NOT EXISTS customers (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  surname TEXT,
  name    TEXT,
  phone   TEXT,
  address TEXT,
  CONSTRAINT chk_surname CHECK (surname IS NOT NULL AND length(surname) <= 30),
  CONSTRAINT chk_name CHECK (name IS NOT NULL AND length(name) <= 30),
  CONSTRAINT chk_phone CHECK (phone IS NOT NULL AND length(phone) <= 30),
  CONSTRAINT chk_address CHECK (address IS NOT NULL AND length(address) <= 300)
);

CREATE TABLE IF NOT EXISTS deals (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER,
  dttm        timestamp,
  CONSTRAINT chk_customer_frk FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE INDEX IF NOT EXISTS products_ind
  ON products (name);

CREATE INDEX IF NOT EXISTS customers_ind
  ON customers (id);

CREATE INDEX IF NOT EXISTS deals_ind
  ON customers (id);

