-- from -- http://en.wikibooks.org/wiki/SQL_Exercises/Planet_Express
-- but with lowercase table and column names

CREATE TABLE Employee (
  employee_id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  position TEXT NOT NULL,
  salary REAL NOT NULL,
  remarks TEXT
);

CREATE TABLE Planet (
  planet_id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  coordinates REAL NOT NULL
);

CREATE TABLE Shipment (
  shipment_id INTEGER PRIMARY KEY NOT NULL,
  date TEXT,
  manager_id INTEGER NOT NULL
    CONSTRAINT fk_employee_employee_id REFERENCES Employee(employee_id),
  planet_id INTEGER NOT NULL
    CONSTRAINT fk_planet_planet_id REFERENCES Planet(planet_id)
);

CREATE TABLE HasClearance (
  employee_id INTEGER NOT NULL
    CONSTRAINT fk_employee_employee_id REFERENCES Employee(employee_id),
  planet_id INTEGER NOT NULL
    CONSTRAINT fk_planet_planet_id REFERENCES Planet(planet_id),
  level INTEGER NOT NULL,
  PRIMARY KEY(employee_id, planet_id)
);

CREATE TABLE Client (
  account_number INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL
);

CREATE TABLE Package (
  shipment_id INTEGER NOT NULL
    CONSTRAINT fk_shipment_shipment_id REFERENCES Shipment(shipment_id),
  package_number INTEGER NOT NULL,
  contents TEXT NOT NULL,
  weight REAL NOT NULL,
  sender_id INTEGER NOT NULL
    CONSTRAINT fk_Client_account_number REFERENCES Client(account_number),
  recipient_id INTEGER NOT NULL
    CONSTRAINT fk_Client_account_number REFERENCES Client(account_number),
  PRIMARY KEY(shipment_id, package_number)
);
