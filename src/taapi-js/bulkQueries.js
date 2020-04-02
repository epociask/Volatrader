const taapi = require("taapi");
const _ = require('lodash')
const db = require('./db')
const indicators = require("./indicators.json")


const secret = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtcG9jaWFza0Bkb25zLnVzZmNhLmVkdSIsImlhdCI6MTU4MzMxNzYwNSwiZXhwIjo3ODkwNTE3NjA1fQ.hfTvshR4HJuCSJ4XJNEgb_xkWIuW0ixZXm7OthcwUFk"
const client = taapi.client(secret);

// Init bulk queries. This resets all previously added queries
client.initBulkQueries();

// Get the BTC/USDT rsi, ao, adx, cmf, macd, atr, rsi 5 hours ago, 50 MA values on the 1 hour time frame from binance


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let indResults = {}

function cleanIndResult(result, indResults){
  result.forEach(ind => {
    indResults[ind.indicator] = ind.result
  })
}

async function makeQueries() {
  let queryList = []
  for(let i=0; i < Object.keys(indicators).length; i++){
    client.addBulkQuery(Object.values(indicators)[i], "binance", "BTC/USDT", "5m")
    if((i+1) % 20 == 0){
      client.executeBulkQueries().then(result => {
        // console.log(result);
        cleanIndResult(result, indResults)
        console.log(JSON.stringify(indResults))
      }).catch(error => {
        console.log(error);
      });
      await sleep(1300)
      client.initBulkQueries();
    }
  }
  console.log(JSON.stringify(indResults))
}

makeQueries()

db('btcusdt_ohlcv_5m')
  .update({
    indicator: indResults
  })
  .then(() => console.log('success'))