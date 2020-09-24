import config
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from get_finance_data import get_yahoo_finance_data
from database.build_database import build_database

# Get the application instance
connex_app = config.connex_app
app = connex_app.app

# Build the database if none exists
app.logger.info('Checking if database file exists')
build_database()

app.logger.info('Adding API swagger definition to connexion')

# Read the swagger.yml file to configure the endpoints
options = {"swagger_ui": True if connex_app.app.env == 'development' else False}
connex_app.add_api("swagger.yml", options=options)

app.logger.info('API swagger endpoints configured succesfully')

app.logger.info('Starting background scheduler for get finance data job')

scheduler = BackgroundScheduler()
scheduler.add_job(func=get_yahoo_finance_data, trigger="interval", minutes=1)
scheduler.start()

app.logger.info('Background scheduler for get finance data job started successfully')

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    connex_app.run(debug=True if connex_app.app.env == 'development' else False)