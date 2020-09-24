from models.ohlc import OHLC # pylint: disable=F0401
from datetime import datetime

# returns a mock database query response
def mock_db_query(*args, **kwargs):
    class MockResponse(OHLC):
        def __init__(self, created_at, data_id, s_close, s_high, s_low, s_open, s_volume, symbol, timestamp, updated_at):
            super(MockResponse, self).__init__()
            self.created_at = created_at
            self.data_id = data_id
            self.s_close = s_close
            self.s_high = s_high
            self.s_low = s_low
            self.s_open = s_open
            self.s_volume = s_volume
            self.symbol = symbol
            self.timestamp = timestamp
            self.updated_at = updated_at
    
    return [MockResponse(datetime.strptime('2020-09-24T14:37:44.181335', '%Y-%m-%dT%H:%M:%S.%f'), 1133, 107.91999816894531, 107.91999816894531, 107.91999816894531, 107.91999816894531, 0.0, 'AAPL', datetime.strptime('2020-09-24T14:37:44.181335', '%Y-%m-%dT%H:%M:%S.%f'), datetime.strptime('2020-09-24T14:37:44.181335', '%Y-%m-%dT%H:%M:%S.%f'))]