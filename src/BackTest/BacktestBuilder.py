import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os 
from Helpers.Constants.Enums import *
from termcolor import colored

def figures_to_html(figs, filename="dashboard.html"):
    if os.path.exists(filename):
        os.remove(filename) #this deletes the file
    dashboard = open(filename, 'w')
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")
    return filename

def getBacktestResultsString(strategy, candleSize: Candle, pair: Pair, principle: int, endValue: float, totalPl: float, totalTrades, startDate, endDate, profitable, unprofitable , stopLoss, takeProfit):

    valColor = 'green' if endValue > principle else 'red'
    finalValStr = colored(str(endValue), valColor, attrs=['bold'])
    totalPlStr = colored(str(totalPl), valColor, attrs=['bold']) 
    returnString = ""
    returnString+=f"\t\tResults for {strategy}"
    returnString+=f"\n\t\tPair: {pair.value}"
    returnString+=f"\n\t\tCandle Size: {candleSize.value}"
    returnString+=f"\n\t\t'Starting Principle Amount: ${str(principle)}"
    returnString+=f"\n\t\tFinal Portfolio Value: ${finalValStr}"
    returnString+=f"\n\t\tTotal PnL: {totalPlStr}%"
    returnString+=f"\n\t\tTotal Trades: {totalTrades}"
    returnString+=f"\n\t\tStarting Backtest at: {startDate}"
    returnString+=f"\n\t\tEnding Backtest at: {endDate}"
    returnString+=f"\n\t\tNumber of Profitable Trades: {colored(profitable, 'green')}"
    returnString+=f"\n\t\tNumber of Unprofitable Trades {colored(unprofitable, 'red')}"
    returnString+=f"\n\t\tTake Profit: {takeProfit}%"
    returnString+=f"\n\t\tStop Loss: {stopLoss}%"

    return returnString


def generateGraphs(candle_data: pd.DataFrame, pair: Pair, candle: Candle, stratString: str):

    candle_data.index = pd.to_datetime(candle_data['timestamp'])
    del candle_data['timestamp']
    fig = make_subplots(rows=1, cols=1)
    fig1 = make_subplots(rows=1, cols=1)
    fig1.add_trace(go.Scatter(x = candle_data.index,
                              y = candle_data['principle'],
                              name = "Principle"
                              ))

    fig.update_layout(
        title={
            'text': f"BACKTEST SUMMARY FOR {pair.value}/{candle.value} with {stratString}",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig.add_trace(go.Candlestick(x=candle_data.index, yaxis="y2",
                        open=candle_data['open'],
                        high=candle_data['high'],
                        low=candle_data['low'],
                        close=candle_data['close'],
                        name="CANDLES"))
    
    fig.add_trace(go.Scatter(x=candle_data.index, y=candle_data['buy'], yaxis="y2", mode='markers', line=dict(color='royalblue', width=4), name = "BUY"))
    fig.add_trace(go.Scatter(x=candle_data.index, y=candle_data['sell'], yaxis="y2", mode='markers', line=dict(color='yellow', width=4), name="SELL"))

    # fig2 = make_subplots(rows=1 , cols=1)
    fig.add_trace(go.Line(x=candle_data.index, yaxis="y2",
                           y=candle_data['sma_5'],
                           name="SMA_5"))

    fig.add_trace(go.Line(x=candle_data.index, yaxis="y2",
                           y=candle_data['sma_8'],
                           name="SMA_8"))

    fig.add_trace(go.Line(x=candle_data.index, yaxis="y2",
                           y=candle_data['sma_15'],
                           name="SMA_15"))

    fig.add_trace(go.Bar(x = candle_data.index, yaxis="y",
                        y = candle_data['volume']))

    fig1.update_layout(
        title={
            'text': "PRINCIPLE SUMMARY",
            'y':0.9,
            'x':0.5,
        }
    )

    return [fig, fig1]