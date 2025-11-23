import pandas as pd
class Indicators:
    @staticmethod
    def SMA(df,window):
        df[f"SMA_{window}"] = df['adj_close'].rolling(window).mean() #calculated by adding up the closing prices of an asset over a specific
        # number of periods and dividing by the number of periods
        return df
    @staticmethod
    def EMA(df,window): # trend of an asset by giving more weight to recent price data
        df[f"EMA_{window}"]=df['adj_close'].ewm(span=20, adjust=False).mean()


