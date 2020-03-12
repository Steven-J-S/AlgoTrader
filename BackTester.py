
from SimpleStrategy import Strat_SMA
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

#API KEY
f=open("AlphaVantageAPI.txt", "r")
KEY = f.read()
ts = TimeSeries(key=KEY, output_format='pandas')

#Stock/Market Request Parameters
Market = 'ADBE'
Interval = '1min'
OutPutSize = 'full'

#Load/Pull Data and put in DataFrame
market_data, meta_data = ts.get_daily(symbol=Market,outputsize=OutPutSize)
file_name = '/home/steven/eclipse-workspace/AlgoTrader/SPY.pkl'
benchmark_data = pd.read_pickle(file_name)
df = pd.concat([benchmark_data['4. close'], market_data['4. close']], axis=1, keys=['SPY', Market],sort=True)
df['Signal'] = ''
df['Performance'] = ''

#Monetary capabilities and Restrictions
cap = 10000        #Starting Capital
commission = 0.01  #percentage (change this when adding other instruments, options/cfds)
spread = 0.001   #percentage
leverage = 1    #if leverage is permitted
short = 0       #-1 if short capabilities are permitted

'''
Add List:
Use Differences/Percentages
Plot Cummulative differences
Commissions (simple % or weighted: abs_comm/(cap0-(cap0%stockprice_T))
Spread
Hold signal
Short capabilities
Leverage capabilities
Check if Ticker Exists
Check how long Ticker Exists
Add Universe of Stocks -> PortfolioManager/StockSelector that selects stocks
'''

############
#BACKTESTER#
############

#length of data to feed to strategy/algo
datafeed = 30 
#previous signal, start with N/A
signal_prev = 'NaN'
#Run Strategy Over Data
for i in range(0,len(df) - datafeed):
    #IMPLEMENT YOUR STRATEGY HERE
    signal = Strat_SMA(df[Market][i:i+datafeed])
    #Current and previous prices, previous performance
    PT = df.at[df.index.values[i+datafeed], Market]
    Pt = df.at[df.index.values[i+datafeed-1], Market]
    Perft = df.at[df.index.values[i+datafeed-1], 'Performance']
    Rt = PT - Pt
    
    #Process signal
    if signal == 'buy':
        #First Action
        if signal_prev == 'NaN':
            df.at[df.index.values[i+datafeed], 'Performance'] = PT
        #Consecutive Actions
        elif signal_prev == 'buy':
            df.at[df.index.values[i+datafeed], 'Performance'] = Perft + Rt
        elif signal_prev == 'sell':
            df.at[df.index.values[i+datafeed], 'Performance'] = Perft
            
        #Reset Signals
        df.at[df.index.values[i+datafeed], 'Signal'] = signal
        signal_prev = signal
    elif signal == 'sell': #ammend with shortselling !='sell'
        #First Action
        '''
        if signal_prev == 'NaN':
            df.at[df.index.values[i+datafeed], 'Performance'] = PT
        '''
        #Consecutive Actions
        if signal_prev == 'buy':
            df.at[df.index.values[i+datafeed], 'Performance'] = Perft + Rt
        elif signal_prev == 'sell':
            df.at[df.index.values[i+datafeed], 'Performance'] = Perft
        
        #Reset Signals
        df.at[df.index.values[i+datafeed], 'Signal'] = signal
        signal_prev = signal
    else :
        df.at[df.index.values[i+datafeed], 'Signal'] = signal
        signal_prev = signal

#Remove rows with empty cells, convert to cumulative returns
df = df.iloc[datafeed:]
df.drop('Signal', axis=1, inplace=True) #Eventually remove entirely
df['SPY'] = df['SPY']/df.at[df.index.values[0], 'SPY']
df[Market] = df[Market]/df.at[df.index.values[0], Market]
df['Performance'] = df['Performance']/df.at[df.index.values[0], 'Performance']
print(df)
#Plot
df.plot()
plt.show()



