from app import appInstance, db
from app.forms import LoginForm, RegistrationForm, TradeForm, RollForm
from app.models import User, Trade, TradeLeg
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

import app.utils_routes as rhelp

@appInstance.route('/')
@appInstance.route('/index')
@login_required
def index():
    user = User.query.filter_by(username = current_user.username).first()
    trades = user.trades.order_by(Trade.open_date.desc()).all()
    return render_template('index.html', title="Home", trades=trades)

@appInstance.route('/statistics')
@login_required
def statistics():
    user = User.query.filter_by(username = current_user.username).first()
    trades = user.trades.order_by(Trade.open_date.desc()).all()
    stats = rhelp.getStats(trades)
#    plotCountByStrat = rhelp.getBarChart(stats['countByStrat'], 'Counts by strategy')
    plotCountByStrat = rhelp.getCountByStratChart(stats['countByStrat'], 'Counts by strategy')
    plotCountByTicker = rhelp.getCountByStratChart(stats['countByTicker'], 'Counts by ticker')
#    plotCountByTicker = rhelp.getBarChart(stats['countByTicker'], 'Counts by ticker')
    plotPnlByStrategy = rhelp.getBarChart(stats['pnlByStrat'], 'P/L by strategy')
    plotPnlByTicker = rhelp.getBarChart(stats['pnlByTicker'], 'P/L by ticker')
    return render_template('statistics.html', stats = stats, figureCountsByStrat = plotCountByStrat, \
        figureCountsByTicker = plotCountByTicker, figurePnlByStrategy = plotPnlByStrategy, \
        figurePnlByTicker = plotPnlByTicker)

@appInstance.route('/addTrade', methods = ['GET', 'POST'])
@login_required
def addTrade():
    formInstance = TradeForm()
    if formInstance.validate_on_submit():
        newPlayId = rhelp.getPlayId(formInstance.playid.data, formInstance.ticker.data)
        tradeStatus = rhelp.getTradeStatus(formInstance.close_date.data, formInstance.close_premium.data)
        tradeComment = rhelp.getTradeComment(formInstance.comment.data)
        user = User.query.filter_by(username = current_user.username).first()
        newTrade = Trade(ticker = formInstance.ticker.data, playid = newPlayId, strategy = formInstance.strategy.data,\
            status = tradeStatus,\
            no_contracts = formInstance.no_contracts.data, no_legs = formInstance.no_legs.data,\
            comment = tradeComment, open_date = formInstance.open_date.data,\
            open_premium = formInstance.open_premium.data, open_underlying = formInstance.open_underlying.data,\
            close_date = formInstance.close_date.data, close_premium = formInstance.close_premium.data,\
            close_underlying = formInstance.close_underlying.data, pnl = formInstance.pnl.data,\
            dailypnl = formInstance.dailypnl.data, holder = user)
        tradeLegsForDb = []
        for idx in range(formInstance.no_legs.data):
            entry = formInstance.legs.entries[idx]
            if not rhelp.validateTradeLegEntry(entry):
                flash("Trade leg input faulty", 'danger')
                return redirect(url_for('addTrade'))
            tradeLegsForDb.append(TradeLeg(opened = entry.opened.data, size = entry.size.data,\
                contract_type = entry.contract_type.data, strike = entry.strike.data, expiry = entry.expiry.data,\
                trade = newTrade))
        db.session.add(newTrade)
        for leg in tradeLegsForDb:
            db.session.add(leg)
        db.session.commit()
        flash('Successful new trade created for ' + current_user.username, 'success')
        return redirect(url_for('index'))
    return render_template('addTrade.html', title = 'Add new trade', form = formInstance)

@appInstance.route('/edit/<id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    formInstance = TradeForm()
    trade = Trade.query.filter_by(playid = id).first()
    # fill out form fields with existing data
    if request.method == 'GET':
        rhelp.populateTradeForm(formInstance, trade)
    if formInstance.validate_on_submit():
        rhelp.editTradeFromForm(formInstance, trade)
        db.session.commit()
        flash('Successful edit of ' + trade.ticker, 'success')
        return redirect(url_for('index'))
    return render_template('editTrade.html', playid = id, form = formInstance)

@appInstance.route('/roll/<id>', methods = ['GET', 'POST'])
@login_required
def roll(id):
    formInstance = RollForm()
    trade = Trade.query.filter_by(playid = id).first()
    if request.method == 'GET':
        rhelp.populateRollForm(formInstance, trade)
    if formInstance.validate_on_submit():
        trade.comment = rhelp.getTradeComment(formInstance.comment.data)
        trade.open_premium = round(trade.open_premium + float(formInstance.roll_premium.data), 2)
        tradeLegsForDb = []
        for idx in range(trade.no_legs):
            entry = formInstance.legs.entries[idx]
            if not rhelp.validateTradeLegEntry(entry):
                flash("Trade leg input faulty", 'danger')
                return redirect(url_for('index')) # TODO: redirect to same roll page
            tradeLegsForDb.append(TradeLeg(opened = entry.opened.data, size = entry.size.data,\
                contract_type = entry.contract_type.data, strike = entry.strike.data, expiry = entry.expiry.data,\
                trade = trade))
        for leg in tradeLegsForDb:
            db.session.add(leg)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('rollTrade.html', playid = id, form = formInstance)

@appInstance.route('/delete/<id>')
@login_required
def delete(id):
    trade = Trade.query.filter_by(playid = id).first()
    legs = trade.legs.all()
    for leg in legs:
        db.session.delete(leg)
    db.session.delete(trade)
    db.session.commit()
    return redirect(url_for('index'))

@appInstance.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    formInstance  = LoginForm()
    if formInstance.validate_on_submit():
        user = User.query.filter_by(username = formInstance.username.data).first()
        if user is None or not user.check_password(formInstance.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = formInstance.rememberMe.data)
        nextPage = request.args.get('next')
        if not nextPage or url_parse(nextPage).netloc != '':
            return redirect(url_for('index'))
        return redirect(nextPage)
    return render_template('login.html', title = 'Sign In', form = formInstance)

@appInstance.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@appInstance.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    formInstance = RegistrationForm()
    if formInstance.validate_on_submit():
        newUser = User(username = formInstance.username.data, email = formInstance.email.data)
        newUser.set_password(formInstance.password.data)
        db.session.add(newUser)
        db.session.commit()
        flash('Congratulations, registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = formInstance)

@appInstance.route('/jsontest')
@login_required
def jsonTest():
    people = {
        'name': 'Edward Teller',
        'field': 'Nuclear Physics',
        'country': 'Hungary'
    }

    return people