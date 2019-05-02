#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
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
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Setup the tests"""
        # Remove JSON file if any
        try:
            os.remove('file.json')
        except Exception as e:
            pass

        dict_values = {'first_name': 'Bobby',
                       'last_name': 'Wow', 'email': 'bobbyw@gmail.com'}
        cls.new = User(**dict_values)
        cls.new.save()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_valid_get(self):
        """Tests when get is called with valid parameters"""
        storage = FileStorage()
        actual = storage.get(self.new.__class__.__name__, self.new.id)
        expected = self.new
        self.assertEqual(expected, actual)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_invalid_get(self):
        """Tests when get is called with invalid parameters"""
        storage = FileStorage()
        # Tests when wrong id is given
        actual = storage.get(self.new.__class__.__name__, '12')
        expected = None
        self.assertEqual(expected, actual)

        # Tests when wrong class is given
        actual = storage.get('Place', self.new.id)
        self.assertEqual(expected, actual)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_valid_count(self):
        """Tests when count is called with valid parameters"""
        # Tests when no parameters are passed"""
        storage = FileStorage()
        storage.save()
        with open('file.json', 'r') as f:
            js = f.read()
        json_dict = json.loads(js)
        expected = len(json_dict)
        actual = storage.count()
        self.assertEqual(expected, actual)

        list_cls = ['State', 'City', 'User', 'Amenity', 'Place', 'Review']
        for cls in list_cls:
            expected = 0
            for item in json_dict.values():
                if item['__class__'] == cls:
                    expected = expected + 1
            actual = storage.count(cls)
            self.assertEqual(expected, actual)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_invalid_count(self):
        """Tests when count is called with invalid parameters"""
        invalid = ['AWER', 12, 12.4, (2, 3), [124, 2], {'hi': 5}]
        storage = FileStorage()
        expected = 0
        for test in invalid:
            actual = storage.count(test)
            self.assertEqual(expected, actual)
