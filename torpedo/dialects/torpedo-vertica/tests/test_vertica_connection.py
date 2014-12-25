__author__ = 'kbroughton'

import unittest
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker, mapper
from sqlalchemy.sql import text

import yaml
import os

yaml.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       os.getcwd()))
engine = None
base = declarative_base()

class TestClassicalMapping(unittest.TestCase):

    metadata = MetaData()
    engine = sa.create_engine("vertica+pyodbc://dbadmin:dbadmin@vertica_deploy_test_db")
    Session = sessionmaker(bind=engine)
    _session = Session()

    classical_users = Table('classical_users', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('fullname', String(50)),
            Column('password', String(12)),
            __table_args__ = { 'schema': 'sqlatest' }
        )

    # Classical mapping class inherits from object, not Base
    class Users(object):
        def __init__(self, name, fullname, password):
            self.name = name
            self.fullname = fullname
            self.password = password

    mapper(Users, classical_users)

    metadata.drop_all(engine, checkfirst=True)
    metadata.create_all(engine)

    def test_classical_raw_insert_sqlapi_query(self):

        self.engine.execute(text("INSERT INTO classical_users ( name , fullname, password ) VALUES ('a', 'a Jones', 'a_password')"))
        a_user_pwd = self._session.query(self.Users.password).filter_by(name='a').scalar()
        print("Found user_id for user with name a: " + a_user_pwd)
        self.assertEqual(a_user_pwd, 'a_password')

    def test_classical_raw_insert_raw_query(self):

        self.engine.execute(text("INSERT INTO classical_users ( name , fullname, password ) VALUES ('b', 'b Jones', 'b_password')").\
                        execution_options(autocommit=True))
        result = self.engine.execute(text("SELECT password FROM classical_users WHERE name = 'b'")).scalar()
        print("Found user_id for user with name b: " + result)
        self.assertEqual(result, 'b_password')

    def test_classical_sqlapi_inline_insert_raw_query(self):
        """Currently failing because the insert does not work.
            SQLAlchemy creates a Insert(ValueBase) object that adds a column and generated value to the insert
            statement causing vertica to fail "Cannot insert into Identity/Auto_increment"""

        self.classical_users.insert(inline=True, values={'name': 'c', 'fullname': 'c Jones', 'password': 'c_password'})
        result = self.engine.execute(text("SELECT password FROM classical_users WHERE name = 'c'")).scalar()
        print("Found user_id for user with name c: " + str(result))
        self.assertEqual(result, 'c_password')

    def test_declarative_reflection(self):
        pass

class TestDeclarativeReflection(unittest.TestCase):

    class User(base):
        __tablename__ = 'users_declarative_table'
        id = Column(Integer, primary_key=True, autoincrement=False)
        name = Column(String)
        fullname = Column(String)
        password = Column(String)
        addresses = relationship("Address", backref="user")

        # __table_args__ = (
        #       { 'schema': 'sqlatest' }
        #     )
        def __repr__(self):
            return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)


    class Address(base):
        __tablename__ = 'addresses_declarative_table'
        id = Column(Integer, primary_key=True, autoincrement=False)
        email_address = Column(String, nullable=False)
        user_id = Column(Integer, ForeignKey('users_declarative_table.id'))

#        user = relationship("User", backref=backref('addresses_declarative_table', order_by=id))
        # __table_args__ = (
        #       { 'schema': 'sqlatest' }
        #     )
        def __repr__(self):
            return "<Address(email_address='%s')>" % self.email_address


    @classmethod
    def setUpClass(cls):
        standard_connect = False

        if standard_connect:
            cls._engine = sa.create_engine(sa.engine.url.URL(
                drivername=conf.drivername,
                username=conf.username,
                password=secrets.password,
                host=conf.host,
                database=conf.database,
            ))
        else:
            cls._engine = sa.create_engine("vertica+pyodbc://dbadmin:dbadmin@vertica_deploy_test_db")

        cls._meta = sa.MetaData()
        cls._base = base

        cls._base.metadata.drop_all(cls._engine, checkfirst=True)
        cls._base.metadata.create_all(cls._engine)

        Session = sessionmaker(bind=cls._engine)
        cls._session = Session()

    def test_connection(self):
        self.assertEqual(self._engine.connect()._connection_is_valid, True)

    def test_reflection(self):
        """
        Reflection allows us to define mapped classes using info in database system tables
        rather than manually specifying the mapping.
        """
        standard_connect = False

        if standard_connect:
            self._engine = sa.create_engine(sa.engine.url.URL(
                drivername=conf.drivername,
                username=conf.username,
                password=secrets.password,
                host=conf.host,
                database=conf.database,
            ))
        else:
            self._engine = sa.create_engine("vertica+pyodbc://dbadmin:dbadmin@vertica_deploy_test_db")


        desc = sa.Table('users_declarative_table', self._meta, autoload=True, autoload_with=self._engine)
        all_table_columns = [c.name for c in desc.columns]

        self.assertEqual(set(['id', 'name', 'fullname', 'password']), set(all_table_columns) )



    def test_declarative_relationship(self):
        """
        Using two tables test that each can access and modify the other
        """
        a_user = self.User(id=1, name='a', fullname='a Jones', password='a_password')
        self._session.add(a_user)
        self._session.flush()
        a_user_id = self._session.query(self.User.id).filter_by(name='a').scalar()

        a_direct_address = self.Address(id=1, email_address='a@gmail.com', user_id=a_user_id)
        self._session.add(a_direct_address)
        self._session.flush()

        for instance in self._session.query(self.User).order_by(self.User.id):
            self.assertEqual(instance.name, 'a')
            print (instance.name, instance.fullname)

        for instance in self._session.query(self.Address).filter(self.Address.user == a_user).order_by(self.Address.id):
            self.assertEqual(instance.email_address, 'a@gmail.com')
            print (instance.email_address, instance.user_id)

    def test_schema(self):
        query = "SELECT CURRENT_SCHEMA()"
        result = self._engine.execute(query)
        print(result.fetchone())

        query = "SET SEARCH_PATH TO oig_3_partial_10k_1_0_1"
        result = self._engine.execute(query)

        query = "SELECT CURRENT_SCHEMA()"
        result = self._engine.execute(query)
        print(result.fetchone())

# __table_args__ = {'schema' : 'test'}
    @classmethod
    def tearDownClass(cls):
        cls._engine = None

if __name__ == '__main__':
    unittest.main()
