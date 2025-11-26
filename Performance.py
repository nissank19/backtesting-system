import numpy


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





