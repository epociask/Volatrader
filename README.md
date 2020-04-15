<<<<<<< HEAD
# The Volatrader

--- author/creator =  @epociask ---
--- author/creator = @a-drain ---

## Installation
1. Clone the repo
2. Create a python 3.7+ [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
environment or a python virtualenv (do this so you dont have to worry about non-compatible dependencies/python versions and shit, can get annoying to deal with)
3. Run `pip install -r requirements.txt` to get all the deps ya need
4. Run something! Examples commands down below :)

## Components
1. [Backtester](#Backtester)
2. [PaperTrader](#PaperTrader)
3. [LiveTrader](#LiveTrader)
4. [DataBase](#DataBase)


## Backtester
To run a backtest, make sure you're in `src/BackTest` and run the following:
```bash
python Backtester.py -p <Pair> --candleSize <candlesize> --strategy <strategy> -sl <stoploss percentage> -tp <take profit percentage> --principle <principle> --readFromDatabase <optional; false> --outputGraph True -t <timet to backtest on>
```

## PaperTrader
To start a paper trading instance, run the following replacing <> with your own params
```bash
python PaperTraderDriver.py --pair <pair> --candlesize <candlesize> --strategy <strat> -sl <stoploss> -tp <takeprofit> -pr <principle>   
```

## LiveTrader
Yet to be implemented; Let's figure out a working strat before we blow all of our cash ;)


## DataBase
### To Access
Ensure [postgresql](https://www.postgresql.org/download/) is installed


### Digital Ocean Database login info
TODO: Move this info somewhere a bit more secure
```
[postgresql]
user=doadmin
password=imt6kws2bm7ffay8
host=coin-do-user-7113675-0.db.ondigitalocean.com
port=25060
database=defaultdb

```


### HELPFUL LINKS

- [High Level Architecture Diagram](https://www.draw.io/#G1G2SjvvMVBpf-aHM6BmQZrGi0ucy79wNO)
- [CCXT](https://github.com/ccxt/ccxt)
- [Medium article about writing a trading bot with python lol](https://medium.com/@maxAvdyushkin/writing-crypto-trading-bot-in-python-with-telegram-and-ccxt-80632a00c637)
- [Medium article about using ccxt](https://medium.com/coinmonks/python-scripts-for-ccxt-crypto-candlestick-ohlcv-charting-data-83926fa16a13)

