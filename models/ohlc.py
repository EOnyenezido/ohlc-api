from config import db, ma # pylint: disable=F0401
from datetime import datetime

# SQLAlchemy data model to save OHLC data obtained from financial provider
class OHLC(db.Model):
    __tablename__ = 'ohlc'
    data_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    timestamp = db.Column(db.DateTime)
    symbol = db.Column(db.String(32), index=True)
    s_open = db.Column(db.Float)
    s_high = db.Column(db.Float)
    s_low = db.Column(db.Float)
    s_close = db.Column(db.Float)
    s_volume = db.Column(db.Float)

# Marshmallow schema for the above class to allow serialization and de-serialization
class OHLCSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OHLC
        load_instance = True