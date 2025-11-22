import yfinance as yf
import pandas as pd
import numpy as np
class Data_loader:
    def __init__(self,ticker,start="2010-01-01",end=None):
        self.ticker=ticker
        self.start=start
        self.end=end

    def load (self):
     df=yf.download(self.ticker,self.start,self.end)
     df=df.reset_index() #makes a new column
     df["Date"]=pd.to_datetime(df["Date"])
     ##print(df.dtypes)
     df=df.sort_values(by="Date") #sort by date
     df = df.reset_index(drop=True) #the inital dataframe has not order
     df.ffill() #to fill the mossing values with what was previous
     df.rename(columns={"adj close":"adj_close"})
     return df

    def returns(self,df):
        df['return'] = df['adj_close'].pct_change() #checks the change
        #hv to divide todays by yesterdays
        df['log_return']=np.log((df["adj_close"]/df["adj_close"].shift(1)))
        df = df.dropna(subset=['return', 'log_return']) #drops first cuz both empty
        return df





