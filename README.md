# ohlc-api
A sample application to obtain OHLC data for certain pre-configured financial instruments. It automatically fetches and stores the OHLC information periodically.

#### To quickly run application
1. pip install -r requirements.txt
1. export FLASK_ENV=development **(or set FLASK_ENV=development on Windows)** optional - development enables debug and echo, and gives access to swagger-ui
1. python server.py

#### To run unit tests
1. pip install -r requirements.txt
1. python -m unittest discover tests
