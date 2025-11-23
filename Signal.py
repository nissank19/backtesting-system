import numpy as np
import pandas as pd
from Indicators import Indicators as ind
from data_loader import Data_loader as dl
class Signal:
    @staticmethod
    def generate_emasignal(df, ema_col):

        df["signal"] = 0  # initialize signal column to 0 (hold)

        # shift EMA and price by 1 day to avoid lookahead bias
        prev_price = df['adj_close'].shift(1)
        prev_ema = df[ema_col].shift(1)

        # generate signals
        # nested np.where is used to check entire DataFrame at once
        df['signal'] = np.where(df['adj_close'] > prev_ema, 1,  # buy
                                np.where(df['adj_close'] < prev_ema, -1, 0))  # sell or hold

        df['signal'] = df['signal'].shift(1)  # shift signals down by 1 to prevent using future info
        df['signal'] = df['signal'].fillna(0)  # fill first row with 0

        return df

    def inspect(self, df, ema_col):
#check first few
        print(df[['Date', 'adj_close', ema_col, 'signal']].head(10))


if __name__ == "__main__":
    loader = dl("AAPL")
    df = loader.load()
    df = loader.returns(df)
    df = ind.EMA(df, window=10)  # fixed class name
    df = Signal.generate_emasignal(df, "EMA_10")

    nspect = Signal()
    nspect.inspect(df, "EMA_10")
