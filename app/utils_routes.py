from app import db
from app.models import Trade, TradeLeg

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
    """ provides a new playId for the trade"""
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

def getTradeStatus(close_date, close_premium):
    """ determines trade status """
    if close_date and close_premium:
        tradeStatus = "Closed"
    else:
        tradeStatus = "Open"

    return tradeStatus

def getTradeComment(comment):
    """ determines the comment and if none adds one """
    if not comment:
        tradeComment = "N/A"
    else:
        tradeComment = comment
    
    return tradeComment

def populateTradeForm(formInstance, trade):
    """ when editing a trade, prepopulates the form with values from db """
    formInstance.ticker.data = trade.ticker
    formInstance.playid.data = trade.playid
    formInstance.strategy.data = trade.strategy
    formInstance.no_contracts.data = trade.no_contracts
    formInstance.no_legs.data = trade.no_legs
    formInstance.comment.data = trade.comment
    formInstance.open_date.data = trade.open_date
    formInstance.open_premium.data = trade.open_premium
    formInstance.open_underlying.data = trade.open_underlying
    formInstance.close_date.data = trade.close_date
    formInstance.close_premium.data = trade.close_premium
    formInstance.close_underlying.data = trade.close_underlying
    formInstance.pnl.data = trade.pnl
    formInstance.dailypnl.data = trade.dailypnl
    for idx in range(formInstance.no_legs.data):
        formInstance.legs.entries[idx].opened.data = trade.legs[idx].opened
        formInstance.legs.entries[idx].size.data = trade.legs[idx].size
        formInstance.legs.entries[idx].contract_type.data = trade.legs[idx].contract_type
        formInstance.legs.entries[idx].strike.data = trade.legs[idx].strike
        formInstance.legs.entries[idx].expiry.data = trade.legs[idx].expiry

def populateRollForm(form, trade):
    """ when rolling a trade, prepopulates the form with values from db """
    form.ticker.data = trade.ticker
    form.playid.data = trade.playid
    form.strategy.data = trade.strategy
    form.no_contracts.data = trade.no_contracts
    form.no_legs.data = trade.no_legs
    form.comment.data = trade.comment
    form.open_date.data = trade.open_date
    form.open_premium.data = trade.open_premium
    for idx in range(trade.no_legs):
        legIdx = len(trade.legs.all()) - trade.no_legs + idx
        form.legs.entries[idx].opened.data = trade.legs[legIdx].opened
        form.legs.entries[idx].size.data = trade.legs[legIdx].size
        form.legs.entries[idx].contract_type.data = trade.legs[legIdx].contract_type
        form.legs.entries[idx].strike.data = trade.legs[legIdx].strike
        form.legs.entries[idx].expiry.data = trade.legs[legIdx].expiry

def refreshTradeFromForm(trade, formInstance):
    trade.ticker = formInstance.ticker.data
    trade.strategy = formInstance.strategy.data
    trade.no_contracts = formInstance.no_contracts.data
    trade.status = getTradeStatus(formInstance.close_date.data, formInstance.close_premium.data)
    trade.no_legs = formInstance.no_legs.data
    trade.comment = getTradeComment(formInstance.comment.data)
    trade.open_date = formInstance.open_date.data
    trade.open_premium = formInstance.open_premium.data
    trade.open_underlying = formInstance.open_underlying.data
    trade.close_date = formInstance.close_date.data
    trade.close_premium = formInstance.close_premium.data
    trade.close_underlying = formInstance.close_underlying.data
    trade.pnl = formInstance.pnl.data
    trade.dailypnl = formInstance.dailypnl.data

def refreshLegFromForm(tradeLeg, formInstanceEntry):
    tradeLeg.opened = formInstanceEntry.opened.data
    tradeLeg.size = formInstanceEntry.size.data
    tradeLeg.contract_type = formInstanceEntry.contract_type.data
    tradeLeg.strike = formInstanceEntry.strike.data
    tradeLeg.expiry = formInstanceEntry.expiry.data

def editTradeFromForm(formInstance, trade):
    oldNoLegs = trade.no_legs
    refreshTradeFromForm(trade, formInstance)
    if oldNoLegs == formInstance.no_legs.data:
        for idx in range(oldNoLegs):
            refreshLegFromForm(trade.legs[idx], formInstance.legs.entries[idx])
    elif oldNoLegs > formInstance.no_legs.data:
        for idx in range(formInstance.no_legs.data):
            refreshLegFromForm(trade.legs[idx], formInstance.legs.entries[idx])
        for idx in range(oldNoLegs, formInstance.no_legs.data, -1):
            tradeLeg = trade.legs[idx - 1]
            db.session.delete(tradeLeg)
    elif oldNoLegs < formInstance.no_legs.data:
        for idx in range(formInstance.no_legs.data):
            if idx < oldNoLegs:
                refreshLegFromForm(trade.legs[idx], formInstance.legs.entries[idx])
            else:
                tradeLeg = TradeLeg(opened = formInstance.legs.entries[idx].opened.data,\
                    size = formInstance.legs.entries[idx].size.data,\
                    contract_type = formInstance.legs.entries[idx].contract_type.data,\
                    strike = formInstance.legs.entries[idx].strike.data,\
                    expiry = formInstance.legs.entries[idx].expiry.data,\
                    trade = trade)
                db.session.add(tradeLeg)