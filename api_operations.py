from flask import abort
from models.ohlc import OHLC, OHLCSchema
from get_finance_data import symbols
from config import app

# Endpoint handler for GET /ohlc/{symbol}
def get_ticker_data(symbol, start_time, end_time):
    # Log new request
    app.logger.info('Received new request: {symbol} - {start} - {end}'\
        .format(symbol=symbol, start=start_time, end=end_time))
    # Confirm that symbol is supported
    if symbol not in symbols:
        message = 'Invalid symbol provided: {symbol}. Supported symbols are {supp}'\
            .format(symbol=symbol, supp=",".join(symbols))
        app.logger.error(message) # Log error
        return {
            "success": False,
            "message": message
        }, 400 
    
    # Get data from database
    ticker = OHLC.query.filter(OHLC.symbol == symbol, \
        OHLC.timestamp >= start_time, OHLC.timestamp <= end_time) \
            .all()
    
    if ticker is not None and len(ticker) != 0:
        # Serialize data
        ohlc_schema = OHLCSchema(many=True)
        app.logger.info('Successfully processed request: {symbol} - {start} - {end}'\
            .format(symbol=symbol, start=start_time, end=end_time))
        # Return data
        return {
            "success": True,
            "message": "OHLC data obtained successfully",
            "data": ohlc_schema.dump(ticker)
        }
    else:
        # return 404 not found error
        message = 'No data found for symbol: {symbol} in time frame {start_time} to {end_time}' \
                    .format(symbol=symbol, start_time=start_time, end_time=end_time)
        app.logger.warning(message) # Log warning
        return {
            "success": False,
            "message": message
        }, 404