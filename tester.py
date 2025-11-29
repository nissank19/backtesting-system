import unittest
import pandas as pd
from datetime import datetime
from Backtester import backtester
from Performance import Performance
from Signal import Signal
from Indicators import Indicator

class TestBacktestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a small sample dataset manually
        cls.df = pd.DataFrame({
            "Date": pd.date_range(start="2020-01-01", periods=5, freq="D"),
            "adj_close": [100, 101, 102, 101, 103],
            "High_AAPL": [100, 101, 103, 102, 104],
            "Low_AAPL": [99, 100, 101, 100, 102]
        })

        # Compute EMA
        cls.df = Indicator.EMA(cls.df, window=2)  # small window for test
        cls.df = Signal.generate_emasignal(cls.df, "EMA_2")

        # Run backtest
        cls.bt = backtester()
        cls.bt.runback(df=cls.df)

        # Performance object
        cls.perf = Performance(cls.bt.portfolio_value_history)

    def test_total_returns(self):
        total = self.perf.totalreturns()
        self.assertIsInstance(total, float)
        self.assertGreaterEqual(total, -1.0)

    def test_daily_returns_length(self):
        daily = self.perf.get_daily_returns()
        self.assertEqual(len(daily), len(self.bt.portfolio_value_history)-1)

    def test_volatility_positive(self):
        vol = self.perf.volatility()
        self.assertGreaterEqual(vol, 0)

    def test_CAGR(self):
        cagr = self.perf.CAGR(years=1)
        self.assertIsInstance(cagr, float)

    def test_max_drawdown(self):
        max_dd = self.perf.maxdrawdown("2020-01-01", "2020-01-05", self.df)
        self.assertGreaterEqual(max_dd, 0)
        self.assertLessEqual(max_dd, 1)

if __name__ == "__main__":
    unittest.main()
