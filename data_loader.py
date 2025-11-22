import yfinance as yf
import pandas as pd
import numpy as np
class Data_loader:
    def __init__(self,ticker,start="2010-01-01",end=None):
        self.ticker=ticker
        self.start=start
        self.end=end


    def load(self):
        df = yf.download(self.ticker, self.start, self.end, auto_adjust=True)
        df = df.reset_index()  # make Date a column
        # flatten MultiIndex columns
        df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
        df.rename(columns={"Date_": "Date", "Close_AAPL": "adj_close"}, inplace=True)
        df = df.sort_values(by="Date").reset_index(drop=True)
        df = df.ffill()
        return df

    def returns(self,df):
        df['return'] = df['adj_close'].pct_change() #checks the change
        #hv to divide todays by yesterdays
        df['log_return']=np.log((df["adj_close"]/df["adj_close"].shift(1)))
        df = df.dropna(subset=['return', 'log_return']) #drops first cuz both empty
        return df
loader = Data_loader("AAPL")       # create instance
df = loader.load()                 # download and clean data
df = loader.returns(df)            # compute returns
print(df.head())





