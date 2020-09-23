from app import appInstance, db
from app.models import User, Trade, TradeLeg

@appInstance.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Trade': Trade, 'TradeLeg': TradeLeg}