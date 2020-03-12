from alpha_vantage.timeseries import TimeSeries

#API KEY
f=open("AlphaVantageAPI.txt", "r")
KEY = f.read()
ts = TimeSeries(key=KEY, output_format='pandas')

#Benchmark Request Parameters
Ticker = 'SPY'
Interval = '1min'
OutPutSize = 'full'

#Pull Benchmark Data
benchmark_data, meta_data = ts.get_daily(symbol=Ticker,outputsize=OutPutSize)

#Save Data
location = '/home/steven/eclipse-workspace/AlgoTrader/'
filename = 'SPY.pkl'
benchmark_data.to_pickle(location + filename)

#with open(filename + 'json', 'w') as outfile:
#    json.dump(benchmark_data, outfile)
