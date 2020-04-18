import sys, os
from sys import platform
sys.path.append(os.path.dirname(os.getcwd()))
from flask import Flask
from BackTest.BackTester import backTest
from Helpers.Constants.Enums import * 
app = Flask(__name__)



@app.route("/")

def index():
    return "WELCOME TO THE VOLATRADER HOMEPAGE"

@app.route("/<pair>/<candleSize>/<strategy>/<sl>/<tp>/<time>")

def Test(pair, candleSize, strategy, sl, tp, time):
    backTest(Pair[pair], Candle(candleSize), strategy, int(sl), int(tp), principle=1000, timeStart=Time[time])
    return "SUCCESS"
    

if __name__ == "__main__":
    app.run(debug=True)

