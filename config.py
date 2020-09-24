import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from logging.config import dictConfig

basedir = os.path.abspath(os.path.dirname(__file__))
database_file = os.path.join(basedir, 'database/data.db')    

# Configure logging formatter and handlers
# %(funcName)s:%(lineno)d so errors can be traced to exact line
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] | %(levelname)s | %(module)s | %(funcName)s:%(lineno)d | %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file' : {
            'class' : 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'ohlc-app.log',
            'maxBytes': 1048576,
            'backupCount': 3
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file']
    }
})

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

app.logger.info('Successfully initialized connexion app')

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_ECHO'] = True if app.env == 'development' else False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

app.logger.info('Successfully initialized sqlalchemy db')

# Initialize Marshmallow
ma = Marshmallow(app)

app.logger.info('Successfully initialized marshmallow for object serialiazaion and de-serialization')