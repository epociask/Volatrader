# CCXT-TRADER

--- author/creator =  @epociask ---
--- author/creator = @a-drain ---

## ***GENERAL COMPONENTS***
1. [Backtester ](#Backtester)
2. [_LiveTrader_](#LiveTrader)
3. [_DataBase_](#DataBase)
4. [_PaperTrader_](#PaperTrader)



## Backtester
-- In baby phase, will need a lot of work


### TO RUN (for now)
1. Add `BINANCE_API_KEY` and `BINANCE_SECRET_KEY` to your path
2. Make sure you have data in your local DB
2. `py backtester.py`


## LiveTrader
###  *(LIVETRADER)* CCXT TRAILING STOP LOSS (FUNCTIONAL APPROACH)
let's ensure our investments don't crumble when the market decides to move unfavorably :)


#### TO RUN (for now)
1. Ensure your api keys are put in the dictionary objects in ` authent.py `
2. Make sure dependable packages are installed in `requirements.txt`

## DataBase

### To Access
Ensure postgresql is installed

```
[postgresql]
user=doadmin
password=imt6kws2bm7ffay8
host=coin-do-user-7113675-0.db.ondigitalocean.com
port=25060
database=defaultdb

```



### To deploy:
`git push heroku master`

### To ssh into Heroku server:
1. Make sure you've logged into Heroku via `heroku login`
2. Pushing to heroku remote's master branch will deploy the code to Heroku
3. `git push heroku master` will install deps and run
4. `heroku run bash` will open a cli in the server

### HELPFUL LINKS

[https://www.draw.io/#G1G2SjvvMVBpf-aHM6BmQZrGi0ucy79wNO]

https://github.com/ccxt/ccxt]

[https://medium.com/@maxAvdyushkin/writing-crypto-trading-bot-in-python-with-telegram-and-ccxt-80632a00c637]

[https://medium.com/coinmonks/python-scripts-for-ccxt-crypto-candlestick-ohlcv-charting-data-83926fa16a13]



### API KEYS
 
``` eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtcG9jaWFza0Bkb25zLnVzZmNhLmVkdSIsImlhdCI6MTU4MzIyNDIyNywiZXhwIjo3ODkwNDI0MjI3fQ.RzHJZLnEb4HzluravWjaQZg1W9jd7Jl4wDi0lgnY5jc
```
