from talib._ta_lib import SMA



def Strat_SMA(data):
    '''
    Simple moving average strategy
    Feed: nx4 candlestick data (numpy array), n points, 1 stock (OHLC)
    Out: Buy/Sell signal
    '''
    
    #check data
    
    #SMA
    sma = SMA(data)
    
    
    #Signal Condition
    if data[-1] <= sma[-1]:
        signal = 'sell'
    elif data[-1] > sma[-1]:
        signal = 'buy'
    else :
        signal = 'N/A'
        
    return signal