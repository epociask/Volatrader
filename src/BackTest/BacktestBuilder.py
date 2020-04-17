import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os 
from Helpers.Constants.Enums import *
from termcolor import colored
import numpy as np
from Trader.Indicators.IndicatorConstants import getIndicator

def figures_to_html(string, figs, filename="analysis.html"):

    if os.path.exists(filename):
        os.remove(filename) #this deletes the file
    dashboard = open(filename, 'w')
    dashboard.write("<div align=\"left\"><img src=\"logo.png\" alt=\"LOGO BABY\" style=\"width:400px;height:200px;\"></div>")
    dashboard.write(string)
    dashboard.write("<html><head></head><body>" + "\n")
    for fig in figs:
        inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
        dashboard.write(inner_html)
    dashboard.write("</body></html>" + "\n")
    return filename

def getBacktestResultsString(fees, strategy, candleSize: Candle, pair: Pair, principle: int, endValue: float, totalPl: float, totalTrades, startDate, endDate, profitable, unprofitable , stopLoss, takeProfit, stratString: str, indicators: list, html=False):
    stratString = stratString.replace("_", " ").lower().title()
    valColor = 'green' if endValue > principle else 'red'
    totalPl = colored(str(totalPl)+ "%", valColor, attrs=['bold']) if not html else totalPl
    returnString = ""
    returnString+=f"\t\tResults for {strategy}" if not html else ""
    returnString+=f"\n\t\tPair: {pair.value}" if not html else ""
    returnString+=f"\n\t\tCandle Size: {candleSize.value}" if not html else ""
    returnString+= ("<strong>" if html else "") + "\n\t\tStarting Principle: " + ("</strong>" if html else "") + f"${str(principle)}"
    if html:
        returnString = "<h>" +returnString + "</h>"
        returnString = f"<h1 style=\"color: black; font-family=\"Arial Black\"; class=\"dotted\";> <div align=\"center\"  style=\"border:2px solid {valColor}\"> Backtest Summary for {stratString} on {pair.value}/{candleSize.value} </div></h1>" + returnString
    returnString+= ("<h font-family: \"fantasy\"><br><strong>" if html else "") + ("\n\t\tFinal Portfolio Value: ") + ("</strong>" if html else "") + (f"${colored(str(endValue), valColor, attrs=['bold'])}" if not html else f"${endValue}") +  ("</h>" if html else "")
    returnString+=("<h font-family: \'fantasy\'><br><strong>" if html else "") + f"\n\t\tTotal PnL:  " + ("</strong>" if html else "") + str(totalPl) +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tTotal Trades: " + ("</strong>" if html else "") + str(totalTrades) +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tStarting Backtest at: " + ("</strong>" if html else "") + startDate +  ("</h>" if html else "")
    returnString+=  ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tEnding Backtest at:" + ("</strong>" if html else "") + endDate+  ("</h>" if html else "")
    returnString+=("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tProfitable Trades: " + ("</strong>" if html else "") + (colored(str(profitable), 'green') if not html else str(profitable)) +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tUnprofitable Trades: " +("</strong>" if html else "") + (colored(str(unprofitable), 'red') if not html else str(unprofitable)) +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tTake Profit: " + ("</strong>" if html else "") +  f"{takeProfit[1:3]}%" +  ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tStop Loss: " + ("</strong>" if html else "") + f"{stopLoss}%" + ("</h>" if html else "")
    returnString+= ("<h font-family: \'fantasy\'><br><strong>" if html else "") + "\n\t\tTotal Fees: " + ("</strong>" if html else "") + f"${fees}" + ("</h>" if html else "")
    return returnString



# Returns a candlestick graph with buy and sell points
def generateCandleGraph(candle_data: pd.DataFrame, pair: Pair, candle: Candle, stratString: str, indicators: list):

    fig = make_subplots(rows=5, cols=1)
    fig.update_layout(
        autosize=False,
        height=3000,
        width=1500,
        title={
        'text': f"CANDLE STICK GRAPH WITH USED INDICATORS",
        'y':1   ,
        'x':0.5,   
        'font': dict(family="Roboto ", size=14), 
        'xanchor': 'center',
        'yanchor': 'top'})


    color = []
    for index, row in candle_data.iterrows():
        if row['close'] > row['open']:
            color.append('green')
        else:
            color.append('red')

    steps = []
    sliders = []
    for i in range(0, len(fig.data), 3):
        step = dict(
            method="restyle",
            args=["visible", [False] * len(fig.data)],
        )
        step["args"][1][i:i+3] = [True, True]
        steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Time:  "},
            pad={"t": 50},
            steps=steps
        )]
    
    fig.add_trace(go.Candlestick(x=candle_data.index, yaxis="y2",
                    open=candle_data['open'],
                    high=candle_data['high'],
                    low=candle_data['low'],
                    close=candle_data['close'],
                    name="CANDLES"), row=1, col=1)

    fig.add_trace(go.Bar(x=candle_data.index, y=candle_data['volume'], name="Volume", marker=dict(color=color), yaxis='y'), row=2, col=1)

    rowNum = 3

    for indicator in indicators:

        values = getIndicator(indicator)
        if values[0]: 
            if len(values) == 1 and indicator.find('PATTERN') == -1:
                fig.add_trace(go.Scatter(x=candle_data.index, yaxis="y2",
                            y=candle_data[indicator],
                            name=indicator.upper()), row=1, col=1)

            elif indicator.find('PATTERN') != -1:
                fig.add_trace(go.Scatter(x=candle_data.index, yaxis="y2",
                            y=candle_data[indicator],
                            name=indicator.upper(),  mode='markers', line=dict(color='orange', width=14)), row=1, col=1)

            else:
                for val in values:
                    if type(val) is not bool:
                        print("adding for ", val)
                        color = 'red' if val == 'MOVING AVERAGE BB' else 'grey' 
            
                        
                        fig.add_trace(go.Scatter(x=candle_data.index, yaxis="y2",
                            y=candle_data[val], line=dict(color=color, width=1, dash='dot' if val == 'MOVING AVERAGE BB' else 'solid'),
                            name=val.upper()), row=1, col=1)
        
        else:

                print(f"row # {rowNum} adding for {indicator}")

                if len(values) == 1:
                    fig.add_trace(go.Scatter(x=candle_data.index, yaxis=f'y{rowNum}', y=candle_data[indicator], name=indicator), row=rowNum, col=1)

                else:
                    for val in values:
                        if type(val) is not bool:

                            if val == 'MACD Histogram':
                                fig.add_trace(go.Bar(x=candle_data.index, yaxis=f'y{rowNum}', y=candle_data[val], name=val), row=rowNum, col=1)
                                
                            else:
                                fig.add_trace(go.Scatter(x=candle_data.index, yaxis=f'y{rowNum}', y=candle_data[val], name=val), row=rowNum, col=1)

                if indicator.find('RSI') != -1 and indicator.find('DIVERGE') == -1:
                    fig.add_trace(go.Scatter(x=candle_data.index, yaxis=f'y{rowNum}', y=([30] * candle_data['open'].count()),  line=dict(color='black', width=1, dash='dot')), row=rowNum, col=1)
                    fig.add_trace(go.Scatter(x=candle_data.index, yaxis=f'y{rowNum}', y=([70] * candle_data['open'].count()),  line=dict(color='black', width=1, dash='dot')), row=rowNum, col=1)

        rowNum+=1
      
    fig.add_trace(go.Scatter(x=candle_data.index, y=candle_data['buy'], yaxis="y2", mode='markers', line=dict(color='blue', width=14), name = "BUY"), row=1, col=1)
    fig.add_trace(go.Scatter(x=candle_data.index, y=candle_data['sell'], yaxis="y2", mode='markers', line=dict(color='black', width=14), name="SELL"), row=1, col=1)
    # fig.update_layout(sliders=sliders)
    return fig

import Helpers.TimeHelpers
# buytime buyprice, selltime sellprice profitloss
def generateTransactionHistoryTable(results):
    df = pd.DataFrame(results)
    cols = ['<b>Transaction Number</b>']
    cols = cols + [f"<b>{e.capitalize()}</b>" for e in df.columns]

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(cols),
            fill_color='paleturquoise',
            align='left',
            font=dict(color='black', size=14)),
        cells=dict(values=[df.index, df.buytime, df.buyprice, df.selltime, df.sellprice, df.profitloss],
        fill_color='lavender',
        align='left',))
    ])

    fig.update_layout(title={
        'text': "Transaction History"
    })

    return fig


def generateLinePlot(data, y_value, graph_title):
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x = data.index,
                        y = data[y_value],
                        name = y_value.upper()))    

    fig.update_layout(
        autosize=False,
        height=400,
        width=1500,
            title={
                'text': graph_title,
                'y':0.9,
                'x':0.5,
            },
      
    )
    
        
    return fig



def generateGraphs(candle_data: pd.DataFrame, pair: Pair, candle: Candle, stratString: str, results, strategy, pnlOverDays):
    indicators = strategy.indicators
    candleGraph = generateCandleGraph(candle_data, pair, candle, stratString, indicators)
    linePlot = generateLinePlot(candle_data, 'principle', "Principle Over Time")
    transactions = generateTransactionHistoryTable(results)
    dayByday = go.Figure(data=[go.Table(header=dict(values=["Date", "pNl"]),
                 cells=dict(values=[pnlOverDays.index, pnlOverDays.pNl]))
                ])
    dayByday.update_layout(
        autosize=False,
        height=500,
        width=500,
        title={
        'text': f"Day By Day Profits",
        'y':1,
        'x':0.5,   
        'font': dict(family="Roboto ", size=15), 
        'xanchor': 'center',
        'yanchor': 'top'})

             
                     
    return [candleGraph, linePlot, dayByday, transactions]
