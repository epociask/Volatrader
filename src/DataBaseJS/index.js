const taapi = require("taapi")
const _ = require('lodash')
const ccxt = require('ccxt')

const db = require('./db')
const indicators = require("./indicators.json")
const logToDebug = require('./slackLogger')

const secret = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImVtcG9jaWFza0Bkb25zLnVzZmNhLmVkdSIsImlhdCI6MTU4MzMxNzYwNSwiZXhwIjo3ODkwNTE3NjA1fQ.hfTvshR4HJuCSJ4XJNEgb_xkWIuW0ixZXm7OthcwUFk"
const client = taapi.client(secret);

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Init bulk queries. This resets all previously added queries
client.initBulkQueries();

// Get the BTC/USDT rsi, ao, adx, cmf, macd, atr, rsi 5 hours ago, 50 MA values on the 1 hour time frame from binance

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let indResults = {}
let exceededRateLim = false

// Cleans taapi.io's response into an insertable json object
function cleanIndResult(result, indResults){
  result.forEach(ind => {
    indResults[ind.indicator] = ind.result
    if (ind.result.error != undefined && ind.result.error.includes('429')){
      exceededRateLim = true
    }
  })
}


async function makeQueries(pair, candleSize){
  let queries = []
  client.initBulkQueries()
  await sleep(1000)
  for (let i=0; i < Object.keys(indicators).length; i++){
    if ((i+1) % 20 == 0){
      let t = new Date()
      console.log(`STARTING EXECUTE BULK QUERY WITH ${queries.length} queries`)
      queries = []
      await client.executeBulkQueries()
      .then(result => {
        cleanIndResult(result, indResults)
        console.log(exceededRateLim ? "EXCEEDED RATE LIMIT" : "")
        console.log("FINISHED EXECUTING BULK QUERY")
      })
      .catch(err => {
        console.log("ERROR GETTING INDICATORS: ", err)
        logToDebug({
          text:'Error getting indicators from TAAPI.IO: ',
          fields: {
            'Error': err,
          }
        })
      })
      // let reqTime = new Date() - t
      await sleep(1000)
      client.initBulkQueries()
    } else {
      queries.push(client.addBulkQuery(Object.values(indicators)[i], "binance", pair, candleSize))
      console.log(`Adding ${Object.values(indicators)[i]} to bulk queries` )
    }
  }
  console.log(`FINISHED WRITING FOR ${pair} ${candleSize}`)
  return indResults
}



// Get candles from ccxt
async function getCandlesFromCCXT(pair, candleSize){
  let candleData
  const exchange = new ccxt.binance()
  const candles = {}
  if (exchange.has.fetchOHLCV) {
    try {
      candleData = await exchange.fetchOHLCV (pair, candleSize, undefined, 1)
      candleData = candleData[0]
      candles['timestamp'] = candleData[0]
      candles['open'] = candleData[1]
      candles['high'] = candleData[2]
      candles['low'] = candleData[3]
      candles['close'] = candleData[4]
      candles['volume'] = candleData[5]
    } catch (e){
      logToDebug({
        text:'Error getting candles from CCXT: ',
        fields: {
          'error': e,
        }
      })
      throw new Error(e)
    }
  }
  return candles
}


// Inserts all the data to specified table
async function insertData(pair, candleSize){
  console.log(`STARTING DATA INSERTION FOR ${pair} ${candleSize}`)
  let indJSON = await makeQueries(pair, candleSize)
  const {timestamp, open, high, low, close, volume} = await getCandlesFromCCXT(pair, candleSize)
  const tablePair = pair.replace('/', '')
  const query = db(`${tablePair.toLowerCase()}_ohlcv_${candleSize}`)
  .insert({
    timestamp: new Date(timestamp),
    open,
    high,
    low,
    close,
    volume,
    indicators: indJSON
  })

  try {
    await query
    console.log("Successful insertion!")
  } catch (e){
    console.log("Error Writing indicators: ", e)
    logToDebug({
      'text': 'Error writing indicators',
      'fields': {
        'error': e.toString()
      }
    })
  }
  return
}

function didExceedRateLim(){
  if (exceededRateLim){
    logToDebug({
      text: 'Exceeded Rate limit:',
      fields:{
        error: 'expect bad data for ' + new Date().toUTCString()
      }
    })
  }
}


(async function() {
  while (true){
    let t_min = new Date().getMinutes()
    if (t_min == 0 || t_min == 30){
      await sleep(5000)
      let t1 = new Date()
      console.log("INSERTING 5, 15, 30")
      await insertData('ETH/USDT', '5m')
      await insertData('ETH/USDT', '15m')
      await insertData('ETH/USDT', '30m')
      await insertData('BTC/USDT', '5m')
      await insertData('BTC/USDT', '15m')
      await insertData('BTC/USDT', '30m')
      didExceedRateLim()
      let t2 = new Date()
      logToDebug({
        'text': 'Time to write indicator',
        'fields': {
          'time to write': ((t2-t1)/1000).toString(),
        }
      })
      await sleep(1000*61)
    }
    else if (t_min % 15 == 0){
      await sleep(5000)
      console.log("INSERTING 5, 15")
      await insertData('ETH/USDT', '5m')
      await insertData('ETH/USDT', '15m')
      await insertData('BTC/USDT', '5m')
      await insertData('BTC/USDT', '15m')
      didExceedRateLim()
      await sleep(1000*61)
    }
    else if (t_min % 5 == 0){
      await sleep(5000)
      console.log("INSERTING 5")
      await insertData('ETH/USDT', '5m')
      await insertData('BTC/USDT', '5m')
      didExceedRateLim()
      await sleep(1000*61)
    }
  }

})()
