#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Setup the tests"""
        cls.storage = DBStorage()
        cls.storage.reload()
        dict_values = {'first_name': 'Bobby',
                       'last_name': 'Wow', 'email': 'bobbyw@gmail.com',
                       'password': 'HI'}
        cls.new = User(**dict_values)
        cls.storage.new(cls.new)

    @unittest.skipIf('HBNB_TYPE_STORAGE' not in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] != 'db',
                     'Do not test when testing file storage')
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf('HBNB_TYPE_STORAGE' not in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] != 'db',
                     'Do not test when testing file storage')
    def test_valid_get(self):
        """Tests when get is called with valid parameters"""
        actual = self.storage.get(self.new.__class__.__name__, self.new.id)
        expected = self.new
        self.assertEqual(expected, actual)

    @unittest.skipIf('HBNB_TYPE_STORAGE' not in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] != 'db',
                     'Do not test when testing file storage')
    def test_invalid_get(self):
        """Tests when get is called with invalid parameters"""
        # Tests when wrong id is given
        actual = self.storage.get(self.new.__class__.__name__, '12')
        expected = None
        self.assertEqual(expected, actual)

        # Tests when wrong class is given
        actual = self.storage.get('Place', self.new.id)
        self.assertEqual(expected, actual)

    @unittest.skipIf('HBNB_TYPE_STORAGE' not in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] != 'db',
                     'Do not test when testing file storage')
    def test_valid_count(self):
        """Tests when count is called with valid parameters"""
        # Tests when no parameters are passed
        self.storage.save()
        existing = self.storage.all()
        expected = len(existing)
        actual = self.storage.count()
        self.assertEqual(expected, actual)

        list_cls = ['State', 'City', 'User', 'Amenity', 'Place', 'Review']
        for cls in list_cls:
            expected = 0
            for item in existing.values():
                if item.__class__.__name__ == cls:
                    expected = expected + 1
            actual = self.storage.count(cls)
            self.assertEqual(expected, actual)

    @unittest.skipIf('HBNB_TYPE_STORAGE' not in os.environ and
                     os.environ['HBNB_TYPE_STORAGE'] != 'db',
                     'Do not test when testing file storage')
    def test_invalid_count(self):
        """Tests when count is called with invalid parameters"""
        invalid = ['AWER', 12, 12.4, (2, 3), [124, 2], {'hi': 5}]
        expected = 0
        for test in invalid:
            actual = self.storage.count(test)
            self.assertEqual(expected, actual)
