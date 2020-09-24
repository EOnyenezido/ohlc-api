import os
from config import db, app, database_file # pylint: disable=F0401
from models.ohlc import OHLC # pylint: disable=F0401

def build_database():
    # Only create a new sqlite3 database if one does not exist already
    if not os.path.exists('data.db'):
        app.logger.warning('No database found, building new database at ' + database_file)

        # Create the database
        db.create_all()

        app.logger.info('Database built successfully')