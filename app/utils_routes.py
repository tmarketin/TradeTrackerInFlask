from collections import defaultdict

from app import db
from app.models import Trade, TradeLeg

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

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
    if(trade.no_legs > 0):
        for idx in range(formInstance.no_legs.data):
            legIdx = len(trade.legs.all()) - trade.no_legs + idx
            formInstance.legs.entries[idx].opened.data = trade.legs[legIdx].opened
            formInstance.legs.entries[idx].size.data = trade.legs[legIdx].size
            formInstance.legs.entries[idx].contract_type.data = trade.legs[legIdx].contract_type
            formInstance.legs.entries[idx].strike.data = trade.legs[legIdx].strike
            formInstance.legs.entries[idx].expiry.data = trade.legs[legIdx].expiry

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

def getListOfStrategies(trades):
    """ returns an alphabetical list of all strategies used in trades """
    res = []
    for trade in trades:
        if not trade.strategy in res:
            res.append(trade.strategy)
    
    return ["All"] + sorted(res)

def getListOfTickers(trades):
    """ returns an alphabetical list of all tickers used in trades """
    res = []
    for trade in trades:
        if not trade.ticker in res:
            res.append(trade.ticker)
    
    return ["All"] + sorted(res)

def getListOfYears(trades):
    """ returns an alphabetical list of all tickers used in trades """
    res = []
    for trade in trades:
        year = trade.open_date.year
        if not year in res:
            res.append(year)
    
    return ["All"] + sorted(res, reverse=True)

def getTradeRisk(trade):
    risk = 0
    if(trade.strategy == "Cash Secured Put"):
        risk = trade.no_contracts*trade.legs[-1].strike
    elif(trade.strategy == "Put Credit Spread"):
        strikeDiff = abs(trade.legs[-1].strike - trade.legs[-2].strike)
        risk = trade.no_contracts*(strikeDiff - trade.open_premium)
    elif(trade.strategy == "Call Credit Spread"):
        strikeDiff = abs(trade.legs[-1].strike - trade.legs[-2].strike)
        risk = trade.no_contracts*(strikeDiff - trade.open_premium)
    
    return risk

def getStats(trades):
    stats = defaultdict(lambda: 0)
    stats['countByStrat'] = defaultdict(lambda: 0)
    stats['countByTicker'] = defaultdict(lambda: 0)
    stats['pnlByStrat'] = defaultdict(lambda: 0)
    stats['pnlByTicker'] = defaultdict(lambda: 0)
    for trade in trades:
        if not trade.strategy in stats['countByStrat']:
            stats['countByStrat'][trade.strategy] = defaultdict(lambda: 0)
        if not trade.ticker in stats['countByTicker']:
            stats['countByTicker'][trade.ticker] = defaultdict(lambda: 0)
        stats['countTotalTrades'] += 1
        if trade.status == "Open":
            stats['countOpenTrades'] += 1
            stats['countByStratOpen'] += 1
            stats['countByStrat'][trade.strategy]['Open'] += 1
            stats['countByTicker'][trade.ticker]['Open'] += 1
            if trade.strategy == "Stock":
                stats['openStock'] -= trade.open_premium*trade.no_contracts
            elif trade.open_premium > 0:
                stats['openCredit'] += trade.open_premium*trade.no_contracts
                stats['openCreditRisk'] += getTradeRisk(trade)
            else:
                stats['openDebit'] -= trade.open_premium*trade.no_contracts
        else:
            stats['countClosedTrades'] += 1
            stats['pnlTotal'] += trade.pnl
            stats['pnlByStrat'][trade.strategy] += trade.pnl
            stats['pnlByTicker'][trade.ticker] += trade.pnl
            if trade.pnl > 0.0:
                stats['countWinningTrades'] += 1
                stats['pnlGains'] += trade.pnl
                stats['countByStrat'][trade.strategy]['Win'] += 1
                stats['countByTicker'][trade.ticker]['Win'] += 1
            else:
                stats['countLosingTrades'] += 1
                stats['pnlLosses'] -= trade.pnl
                stats['countByStrat'][trade.strategy]['Loss'] += 1
                stats['countByTicker'][trade.ticker]['Loss'] += 1
    
    return stats

def getCountByStratChart(data, chartName):
    keys = []
    countOpen = []
    countWin = []
    countLoss = []
    for key, value in data.items():
        keys.append(key)
        countOpen.append(value["Open"])
        countWin.append(value["Win"])
        countLoss.append(value["Loss"])

    labels = ["Open", "Wins", "Losses"]
    colors = ["#ffc300", "#8bc34a", "#ff5733"]
    data = {
        'strategies' : keys,
        'Open' : countOpen,
        'Wins' : countWin, 
        'Losses' : countLoss
    }
    plot = figure(x_range = keys, plot_height = 250, title = chartName, toolbar_location = None, tools = "")
    plot.vbar_stack(labels, x = 'strategies', width = 0.9, color = colors, source = data, legend_label = labels)

    plot.y_range.start = 0
    plot.x_range.range_padding = 0.1
    plot.xgrid.grid_line_color = None
    plot.axis.minor_tick_line_color = None
    plot.outline_line_color = None
    plot.legend.location = 'top_left'
    plot.legend.orientation = 'vertical'

    return file_html(plot, CDN)

def getBarChart(data, chartName):
    keys = []
    values = []
    for key, value in data.items():
        keys.append(key)
        values.append(value)
    plot = figure(x_range = keys, plot_height = 250, title = chartName, toolbar_location = None, tools = "")
    plot.vbar(x = keys, top = values, width = 0.9)
    plot.xgrid.grid_line_color = None
    #plot.y_range.start = 0
    return file_html(plot, CDN)
  
