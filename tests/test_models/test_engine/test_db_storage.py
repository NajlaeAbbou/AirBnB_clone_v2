#!/usr/bin/python3
""" Module for testing db storage"""
import unittest
import MySQLdb
from os import getenv
from models.state import State
import models


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'db not my choice')
class DBStorage(unittest.TestCase):
    """ Class to test the db storage method"""

    def setUp(self):
        """ Set up test environment """
        self.db = (MySQLdb.connect(user=getenv('HBNB_MYSQL_USER'),
                                   host=getenv('HBNB_MYSQL_HOST'),
                                   passwd=getenv('HBNB_MYSQL_PWD'),
                                   port=3306,
                                   db=getenv('HBNB_MYSQL_DB')))
        self.cursor = self.db.cursor()

    def tearDown(self):
        """ Remove storage file at end of tests """
        self.cursor.close()
        self.db.close()

    def test_new(self):
        """New object is correctly initialized"""
        new_state = State(name="Casablanca")
        self.assertEqual(new_state.name, "Casablanca")

    def test_save(self):
        """ New object is correctly added to the database """
        self.cursor.execute("SELECT COUNT(*) FROM states")
        old_count = self.cursor.fetchall()[0][0]
        new_state = State(name="Casablanca")
        new_state.save()
        self.cursor.execute("SELECT COUNT(*) FROM states")
        new_count = self.cursor.fetchall()[0][0]
        self.assertEqual(old_count, new_count)

    def test_all(self):
        """ __objects is properly returned """
        new = State(name="Casablanca")
        new.save()
        temp = models.storage.all()
        self.assertIsInstance(temp, dict)

    def test_delete(self):
        """ Deletion of an object """
        new = State(name="Casablanca")
        new.save()
        models.storage.delete(new)
        self.assertNotIn(new, models.storage.all().values())

    def test_reload(self):
        """ Reload objects from file """
        new_state = State(name="Casablanca")
        new_state.save()
        models.storage.reload()
        objs = models.storage.all()
        for obj in objs.values():
            self.assertIsInstance(obj, State)
