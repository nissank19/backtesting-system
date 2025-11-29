import numpy
from datetime import datetime
import pandas as pd
from Signal import Signal
import Backtester
import data_loader
from data_loader import Data_loader
from Indicators import Indicator

class Performance():
    def __init__(self,portfolio_value_history):
        self.portfolio_value_history=portfolio_value_history

    def totalreturns(self):
        inital= self.portfolio_value_history[0]
        final= self.portfolio_value_history[-1]
        return (final-inital)/inital

    def get_daily_returns(self):
        daily_returns = []
        for i in range(1, len(self.portfolio_value_history)):
            today = self.portfolio_value_history[i]
            yesterday = self.portfolio_value_history[i - 1]
            daily_returns.append((today / yesterday) - 1)
        return daily_returns

    def volatility(self):
        returns = self.get_daily_returns()
        return numpy.std(returns)

    def sharpratio(self,riskfreerate=0):
        sharpie=(numpy.mean(self.get_daily_returns())-riskfreerate)/numpy.std(self.get_daily_returns())

    def maxdrawdown(self, startdate, enddate, df):

        from dateutil import parser
        COMMON_FORMATS = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d",
                          "%d.%m.%Y", "%b %d %Y", "%B %d, %Y", "%d %b %Y"]

        def parse_to_date(s):
            s = s.strip()
            for fmt in COMMON_FORMATS:
                try:
                    return datetime.strptime(s, fmt).date()
                except ValueError:
                    pass
            return parser.parse(s, dayfirst=True).date()

        start_dt = parse_to_date(startdate)
        end_dt = parse_to_date(enddate)


        mask = (df["Date"] >= pd.Timestamp(start_dt)) & (df["Date"] <= pd.Timestamp(end_dt))
        subset = df.loc[mask]


        prices = subset["High_AAPL"].values
        peak = -float('inf')
        max_dd = 0
        for p in prices:
            peak = max(peak, p)
            dd = (peak - p) / peak
            max_dd = max(max_dd, dd)

        return max_dd

    def CAGR(self,years):
        start=self.portfolio_value_history[0]
        end=self.portfolio_value_history[-1]
        return ((end/start)**(1/years)-1)

##for later implement win rate, rolling volatility

# Initialize backtester
# Load and prepare data
loader = Data_loader("AAPL")
df = loader.load()
df = loader.returns(df)                   # optional, if you calculate returns
df = Indicator.EMA(df, window=10)         # compute EMA
df = Signal.generate_emasignal(df, "EMA_10")  # generate 'signal' column

# Initialize and run backtester
bt = Backtester.backtester()
bt.runback(df=df)  # DataFrame now contains 'signal'

# Create performance object
perf = Performance(bt.portfolio_value_history)

# Compute metrics
total_return = perf.totalreturns()
daily_returns = perf.get_daily_returns()
volatility = perf.volatility()
sharpe = perf.sharpratio(riskfreerate=0)
cagr = perf.CAGR(years=10)
max_dd = perf.maxdrawdown("2010-6-9", "2019-9-6", df)

# Print results
print("Total Return:", total_return)
print("Volatility:", volatility)
print("Sharpe Ratio:", sharpe)
print("CAGR:", cagr)
print("Max Drawdown:", max_dd)










