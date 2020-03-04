# CCXT-TRADER

--- author/creator =  @epociask ---
--- author/creator = @a-drain ---

## ***GENERAL COMPONENTS***
1. [Backtester ](#Backtester)
2. [_LiveTrader_](#LiveTrader)
3. [_DataBase_](#DataBase)


## Backtester
-- In baby phase, will need a lot of work
### TO DO's
- [ ] Add compatibility for multiple strategies
- [ ] Ensure backtests are working properly --debug 
- [ ] Automate backtests 
- [ ] Output backtest result data to a POSTGRESQL table in database
- [ ] Develop strategies to test


### TO RUN (for now)
1. Add `BINANCE_API_KEY` and `BINANCE_SECRET_KEY` to your path
2. `py backtester.py`


## LiveTrader
###  *(LIVETRADER)* CCXT TRAILING STOP LOSS (FUNCTIONAL APPROACH)
let's ensure our investments don't crumble when the market decides to move unfavorably :)

#### TO DO('s)
- [X] Port over logic from past TSL program to be compatible w/ CCXT

    -Make logic significantly more concise... ie reduce # of lines and improve time-complexity
- [ ] Ensure effecient operations --> async concurrency || multithreading
- [X] Ensure multi-exchange compatibility (Binance, kraken,... etc)
- [ ] Write unit tests to ensure proper debug
 - [ ] DEBUGG
- [ ] When sells are made, write data to POSTGRESQL server
- [ ] Deploy on cloud


[https://github.com/ccxt/ccxt]

[https://medium.com/@maxAvdyushkin/writing-crypto-trading-bot-in-python-with-telegram-and-ccxt-80632a00c637]

[https://medium.com/coinmonks/python-scripts-for-ccxt-crypto-candlestick-ohlcv-charting-data-83926fa16a13]


#### TO RUN (for now)
1. Ensure your api keys are put in the dictionary objects in ` authent.py `
2. Make sure dependable packages are installed ` pip install ccxt ` , ` pip install schedule `
3. ``throw RuntimeException()``

## DataBase

### TO DO's
- [ ]  Create an indicator schedule w/ OHLCV data
    - [ ] link all indicator tables by timestamp
- [ ] Deploy schedule on cloud
- [ ] debug

### To Access
Ensure postgresql is installed

```
username = doadmin
password = imt6kws2bm7ffay8
host = coin-do-user-7113675-0.db.ondigitalocean.com
port = 25060
database = defaultdb
sslmode = require

```

### To test
In DBoperations.py
```
x = DBoperations()
x.connect()
x.DBOPERATIONSFUNCTION()
```


### Indicator API Private key 
    ```
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtcG9jaWFza0Bkb25zLnVzZmNhLmVkdSIsImlhdCI6MTU4MzIyNDIyNywiZXhwIjo3ODkwNDI0MjI3fQ.RzHJZLnEb4HzluravWjaQZg1W9jd7Jl4wDi0lgnY5jc
    ```