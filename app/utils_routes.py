from app.models import Trade

def getTradeIdNum(playid):
    [ticker, pid] = playid.split('-')
    return int(pid)

def generateNextPlayId(trades):
    maxPid = 0
    for trade in trades:
        if not trade.playid:
            continue
        pid = getTradeIdNum(trade.playid)
        if(pid > maxPid):
            maxPid = pid
    maxPid = maxPid + 1
    return trades[0].ticker + '-' + f'{maxPid:04d}'

def getPlayId(playid, ticker):
    if not playid:
        trades = Trade.query.filter_by(ticker = ticker).all()
        if not trades:
            newPlayId = ticker + '-0001'
        else:
            newPlayId = generateNextPlayId(trades)
    else:
        newPlayId = playid
    
    return newPlayId

def validateTradeLegEntry(entry):
    formOk = True
    if not entry.size.data or not entry.strike.data or not entry.expiry.data:
        formOk = False

    return formOk