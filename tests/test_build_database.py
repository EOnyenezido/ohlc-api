import os
import unittest
from config import db, app, database_file # pylint: disable=F0401
from database.build_database import build_database # pylint: disable=F0401

class TestBuildDatabase(unittest.TestCase):
    def test_create_new_database_if_none_exists(self):
        """
        GIVEN that the database file does not exist
        WHEN the application is started
        THEN it should create a new database
        """
        # Arrange
        # Remove the database file if it already exits
        if os.path.exists(database_file):
            os.remove(database_file)
        # Act
        build_database()
        # Assert
        self.assertTrue(os.path.exists(database_file))

    def test_does_not_create_new_database_if_one_exists(self):
        """
        GIVEN that the database file already exists
        WHEN the application is started
        THEN it should not create a new database
        """
        # Arrange
        # Create the database file if it does not already exist
        if not os.path.exists(database_file):
            build_database()
        last_modified_time = os.stat(database_file).st_mtime
        # Act
        build_database()
        # Assert
        self.assertEqual(last_modified_time, os.stat(database_file).st_mtime)

if __name__ == '__main__':
    unittest.main()
        