import yfinance as yf
from database.build_database import db
from models.ohlc import OHLC
from config import app

# Add or remove symbols to support more institutions
symbols = ["SPY", "AAPL", "MSFT"]

def get_yahoo_finance_data():
    app.logger.info('Starting download for financial OHLC data for symbols: ' + " ".join(symbols))

    # download data as data frame from yahoo finance
    data = yf.download(
            # tickers list or string as well
            tickers = symbols,
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            period = "1d",
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            interval = "1m",
            group_by = 'ticker',
            # adjust all OHLC automatically
            auto_adjust = True,
            # download pre/post regular market hours data
            prepost = True,
            # use threads for mass downloading? (True/False/Integer)
            threads = True,
            # proxy URL scheme use use when downloading?
            proxy = None
        )

    app.logger.info('Downloading financial OHLC data successfull')

    app.logger.info('Starting data processing and committing to database')
    # Flatten and save data in database
    for i, j in data.iterrows():
        # For only one symbol, the returned dataframe is not grouped
        if len(symbols) == 1:
            entry = OHLC.query.filter(OHLC.timestamp == i, OHLC.symbol == symbols[0]).one_or_none()
            if entry is None:
                # Create database row
                p = OHLC(timestamp=i, symbol=symbols[0], s_open=j['Open'], s_high=j['High'], \
                    s_low=j['Low'], s_close=j['Close'], s_volume=j['Volume'])
                # Add to session
                db.session.add(p) # pylint: disable=no-member
        else:
            # For multiple symbols, the returned dataframe is grouped and needs to be processed per symbol
            for symbol in symbols:
                entry = OHLC.query.filter(OHLC.timestamp == i, OHLC.symbol == symbol).one_or_none()
                if entry is None:
                    # Create database row
                    p = OHLC(timestamp=i, symbol=symbol, s_open=j[(symbol, 'Open')], s_high=j[(symbol, 'High')], \
                        s_low=j[(symbol, 'Low')], s_close=j[(symbol, 'Close')], s_volume=j[(symbol, 'Volume')])
                    # Add to session
                    db.session.add(p) # pylint: disable=no-member

    # Commit the session
    app.logger.info('Committing session to database')
    db.session.commit() # pylint: disable=no-member
    app.logger.info('Session committed successfully')

    app.logger.info('Finance data download and database update completed successfully')