# -- coding: utf-8 --
"""
 sqlalchemy database model for planet_express project

  In sqlalchemy's view of the world, db_session holds the "state"
  of this thread's interactction with the database.
  autoflush  : do model changes get added to session automatically?
  autocommit : do model changes get written to database automatically?
  db_session.flush() outputs to database, but does not complete transaction.
  db_session.commit() completes an atomic transaction (calls .flush() too)

 The interface between the sqlite database and the object API is something like

   sqlite --- engine --- db_session --- PlanetExpressBase
                                        [Employee, Client, Package, ...]

 See ../database/ for the sqlite schemas and default population.

 It works like this (assuming the database is in its initial state) :

   >>> fry = Employee.find_like('name', '%Fry%')
   >>> fry.name
   u'Phillip J. Fry'
   >>> [c.planet.name for c in fry.clearances]
   [u'Omicron Persei 8', u'Decapod X']
   >>> Planet.find_by('name', 'Amazonia').employees_with_clearance
   []
   >>> zapp = fry.shipments[0].senders[0]  # Zapp Brannigan
   >>> for s in zapp.shipments_sent:
   ...   for p in s.packages:
   ...     print "in shipment {}: {:6} kg to {}".format(
   ...             s.shipment_id, p.weight, p.recipient.name)
   in shipment 1:    1.5 kg to Al Gore's Head
   in shipment 4:    5.0 kg to Leo Wong
   in shipment 4:   27.0 kg to Al Gore's Head

 The SqlAlchemy query interface is also supported;
 see http://docs.sqlalchemy.org/en/rel_0_8/orm/tutorial.html#querying
   >>> Employee.query.filter_by(name='Phillip J. Fry').one().name
   u'Phillip J. Fry'

 Raw SQL can be executed like this:
   >>> result = db_session.execute(
   ...          "SELECT * FROM Package WHERE contents != 'Undeclared';")
  >>> list(result)
  [(2, 2, u'A bucket of krill', 2.0, 8, 7)]

 Changing data looks like this:
   >>> mars = Planet.find_by('name', 'Mars')
   >>> mars.coordinates
   32435021.65468
   >>> mars.coordinates += 1
   >>> db_session.flush()         # send changes to database
   >>> result = db_session.execute(
   ...         "SELECT coordinates FROM Planet WHERE name='Mars';")
   >>> list(result)
   [(32435022.65468,)]
   >>> db_session.rollback()      # undo this transaction without commit()

 And creating a new database record looks something like this.
   >>> obama = Client(name = 'Barack Obama')
   >>> db_session.add(obama)      # put new object into session
   >>> db_session.commit()        # change database & end transaction

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from utilities import project_path

DATABASE = 'sqlite:///' + project_path + '/database/planet_express.db'

engine = create_engine(DATABASE)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

class PlanetExpressBase(object):
  """ All of this project's database objects inherit from this class. """

  @declared_attr
  def __tablename__(cls):
    """ Set name of database table from class name """
    # e.g. "class Employee" corresponds to SQL table 'Employee'
    return cls.__name__

  # Define fields in each table for each column automatically,
  # e.g. Employee.name , since Employee table has a 'name' column.
  __table_args__ = {'autoload':True, 'autoload_with': engine}

  @classmethod
  def col(cls, column):
    """ Return given SqlAlchemy column object """
    # e.g. Employee.col('name') is same as Employee.name
    return cls.__dict__[column]

  # Define shortcut methods for querying
  # e.g. Class.filter(...) rather than Class.query.filter(...)
  # for several of query's methods.

  @classmethod
  def filter(cls, *args):
    return cls.query.filter(*args)

  @classmethod
  def filter_by(cls, *args):
    return cls.query.filter_by(*args)

  @classmethod
  def all(cls, *args):
    return cls.query.all(*args)

  @classmethod
  def query_by(cls, column, value):
    """ Return query object with column == value """
    return cls.query.filter(cls.col(column) == value)  

  @classmethod
  def find_by(cls, column, value):
    """ Return database object with column=value """
    # e.g. Employee.find_by('name', 'Philip J. Fry')
    # (Throws an error if there's more than one.)
    return cls.query_by(column, value).one()

  @classmethod
  def find_all_by(cls, column, value):
    """ Return list of database objects with column=value """
    # e.g. Package.find_all_by('weight', 1.5)
    return cls.query_by(column, value).all()

  @classmethod
  def query_like(cls, column, like_value):
    """ Return query with SQL_LIKE(column, like_value) """
    return cls.query.filter(cls.col(column).like(like_value))

  @classmethod
  def find_like(cls, column, like_value):
    """ Return the database object with column LIKE like_value. """
    # e.g. Employee.find_like('name', '%Fry%')
    # (Throw an error if there's more than one.)
    return cls.query_like(column, like_value).one()

  @classmethod
  def find_all_like(cls, column, like_value):
    """ Return list objects with column LIKE like_value. """
    return cls.query_by(column, like_value).all()

  def __repr__(self):
    """ Default object representation """
    # e.g. <Employee name='Philip J. Fry' id=xxxx>
    try:
      return "<{} name='{}' id={}>".format(self.__class__.__name__,
                                         self.name, id(self))
    except:
      return "<{} id={}>".format(self.__class__.__name__, id(self))

Base = declarative_base(cls=PlanetExpressBase)
Base.query = db_session.query_property()

class Employee(Base):
  # columns : employee_id, name, position, salary, remarks
  # relations: shipments, clearances,
  #            planets_delivered_to, allowed_planets
  pass

class HasClearance(Base):
  # columns : employee_id, planet_id, level
  # relations: employee, planet
  pass

class Shipment(Base):
  # columns : shipment_id, date, manager_id, planet_id
  # relations: manager, planet, packages, senders, recipients
  pass

class Planet(Base):
  # columns : planet_id, name, coordinates
  # relations: shipments, clearances,
  #            shipment_managers, employees_with_clearance
  pass

class Package(Base):
  # columns : shipment_id, package_numbers, contents,
  #           weight, sender_id, recipient_id
  # relations: shipment, sender, recipient
  pass

class Client(Base):
  # columns : account_number, name
  # relations: packages_sent, packages_received,
  #            shipments_sent, shipments_received
  pass

# The "declarative relations" below are described in
# docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html .
# These can be listed within the classes, but since all the classes
# haven't been defined yet, one needs to use strings, and I'm not sure
# how that works for Class.__table__.
#
# Looks like many-to-many relations aren't good for editing :
#  look of 'viewonly' in declarative.html :
#  "not a good idea to use [..] “secondary” arg [..] mapped
#   to a class unless the relationship is declared with viewonly=True
#   Otherwise [..] may attempt duplicate INSERT and DELETE"
# I also hit errors when trying to define Client.shipments_sent
# in a 2nd statement, without using the backref="..." syntax.

Shipment.manager = relationship(Employee)
Employee.shipments = relationship(Shipment)

Shipment.planet = relationship(Planet)
Planet.shipments = relationship(Shipment)

HasClearance.employee = relationship(Employee)
Employee.clearances = relationship(HasClearance)

HasClearance.planet = relationship(Planet)
Planet.clearances = relationship(HasClearance)

Package.shipment = relationship(Shipment)
Shipment.packages = relationship(Package)

Package.sender = relationship(Client, 
                   primaryjoin = Package.sender_id == Client.account_number)
Client.packages_sent = relationship(Package, 
                   primaryjoin = Package.sender_id == Client.account_number)

Package.recipient = relationship(Client, 
                   primaryjoin = Package.recipient_id == Client.account_number)
Client.packages_received = relationship(Package, 
                   primaryjoin = Package.recipient_id == Client.account_number)

Employee.planets_delivered_to = relationship(Planet, viewonly=True,
                                       secondary = Shipment.__table__)
Planet.shipment_managers = relationship(Employee, viewonly=True,
                                       secondary = Shipment.__table__)

Employee.allowed_planets = relationship(Planet, viewonly=True,
                                        secondary=Shipment.__table__)
Planet.employees_with_clearance = relationship(Employee, viewonly=True,
                                        secondary=Shipment.__table__)

Shipment.senders = relationship(Client, viewonly=True,
                      secondary = Package.__table__, 
                      secondaryjoin = Package.sender_id == Client.account_number,
                      backref = "shipments_sent")

Shipment.recipients = relationship(Client, viewonly=True,
                    secondary = Package.__table__, 
                    secondaryjoin = Package.recipient_id == Client.account_number,
                    backref = "shipments_received")

if __name__ == "__main__":
    import doctest
    doctest.testmod()

