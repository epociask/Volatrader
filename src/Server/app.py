import sys, os
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from flask import Flask, render_template, request, redirect, url_for
from BackTest.BackTester import backTest
from Helpers.Constants.Enums import *
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from DataBasePY.DBReader import DBReader
from DataBasePY.DBwriter import DBwriter 
from PaperTrader.PaperTrader import PaperTrader
from threading import Thread
app = Flask(__name__)
auth = HTTPBasicAuth()



VOLATRADE_MASTER_PASSWORD=""

users = {
    "ethen": generate_password_hash(VOLATRADE_MASTER_PASSWORD),
    "thomas": generate_password_hash(VOLATRADE_MASTER_PASSWORD),
    "adrian": generate_password_hash(VOLATRADE_MASTER_PASSWORD),
    "vitty" : generate_password_hash(VOLATRADE_MASTER_PASSWORD),
    "riley" : generate_password_hash(VOLATRADE_MASTER_PASSWORD),
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False 

app = Flask(__name__)



@app.route("/")
@auth.login_required
def index():
    return render_template('index.html')

@app.route("/template")
def template():
    return render_template('template.html')

#@app.rout("/results")
# TODO: Homepage of all backtest results ever

@app.route("/results/<pair>/<candleSize>/<strategy>/<sl>/<tp>/<time>/<principle>")
@auth.login_required
def results(pair, candleSize, strategy, sl, tp, time, principle):
    print(request.args)
    backTest(Pair[pair], Candle(candleSize), strategy, int(sl), int(tp), principle=1000, timeStart=Time[time], server=True)
    return render_template('analysis.html')
    
@app.route("/end", methods=['POST', 'GET'])
@auth.login_required
def endPaperTrade():
    if request.method == "POST":
        item = next(request.form.items())
        key, value = item[1], item[0]

        if key == "TERMINATE":
            DBwriter().killPaperTraderSession(value)

        elif key == "DELETE":
            DBwriter().deletePaperTradeSession(value)

        return redirect(url_for("papertradeRoute"))

@app.route("/backtest", methods=['POST', 'GET'])
@auth.login_required
def backtestRoute(): 
    if request.method == 'POST':
        data = request.form
        print(data)
        return redirect(url_for("results", pair=request.form['pair'], candleSize=request.form['candle'], strategy=request.form['strategy'], sl=request.form['stoploss'], tp=request.form['takeprofit'], principle=request.form['principle'], time=request.form['timeStart']))

    return render_template('backtester.html', pairs=pairs, candles=candles, times=times, strategies=strats)


@app.route("/begin/<pair>/<candleSize>/<strategy>/<sl>/<tp>/<time>/<principle>")
@auth.login_required
def start_session(pair, candleSize, strategy, sl, tp, time, principle):
    print(request.args)
    thread = Thread(target=PaperTrader().trade, args=(Pair[pair], Candle(candleSize), strategy, int(sl), int(tp), principle,Time[time].value,))
    thread.start()
    return redirect(url_for(('papertradeRoute')))

@app.route("/papertrade/start", methods=['POST', 'GET'])
def startPaperTrade():
    if request.method == 'POST':
        data = request.form
        print("data being posted ----->", data)
        return redirect(url_for("start_session", pair=request.form['pair'], candleSize=request.form['candle'], strategy=request.form['strategy'], sl=request.form['stoploss'], tp=request.form['takeprofit'], principle=request.form['principle'], time=request.form['timeStart']))
    return render_template('beginpapertrade.html', pairs=pairs, candles=candles, times=times, strategies=strats)


@app.route("/papertrade", methods=['POST', 'GET'])
@auth.login_required
def papertradeRoute():
    sessions = DBReader().getPaperTradeSessions()
    active = []
    unactive = []
    for session in sessions:
        if session['active'] == 'True':
            active.append(session)

        else:
            unactive.append(session)
        

    return render_template('papertrader.html', active_sessions=active, unactive_sessions=unactive)

if __name__ == '__main__':

    try:
        app.run(debug=True)

    except KeyboardInterrupt:
        DBwriter().killPaperTraderSession()
