from app import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    passwordHash = db.Column(db.String(128))
    trades = db.relationship('Trade', backref = 'holder', lazy = 'dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(4), index = True)
    playid = db.Column(db.String(10))
    strategy = db.Column(db.String(64))
    status = db.Column(db.String(6))
    no_contracts = db.Column(db.Integer)
    no_legs = db.Column(db.Integer)
    comment = db.Column(db.String(256), nullable = True)
    pnl = db.Column(db.Float(), nullable = True)
    dailypnl = db.Column(db.Float(), nullable = True)
    open_date = db.Column(db.Date, index = True, default = date.today)
    open_premium = db.Column(db.Float())
    open_underlying = db.Column(db.Float(), nullable = True)
    close_date = db.Column(db.Date, nullable = True)
    close_premium = db.Column(db.Float(), nullable = True)
    close_underlying = db.Column(db.Float(), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    legs = db.relationship('TradeLeg', backref = 'trade', lazy = 'dynamic')

    def __repr__(self):
        return '<Trade {} : {}>'.format(self.playid, self.strategy)

class TradeLeg(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    opened = db.Column(db.String(6))
    size = db.Column(db.Integer)
    contract_type = db.Column(db.String(4))
    strike = db.Column(db.Float())
    expiry = db.Column(db.Date)
    trade_id = db.Column(db.Integer, db.ForeignKey('trade.id'))

    def __repr__(self):
        return '<Leg {} {} {} contracts at {} to expire on {}'.format(self.opened, self.size, self.contract_type,\
            self.strike, self.expiry)