import numpy


class Performance():
    def __init__(self,portfolio_value_history):
        self.portfolio_value_history=portfolio_value_history

    def totalreturns(self):
        inital= self.portfolio_value_history[0]
        final= self.portfolio_value_history[-1]
        return (final-inital)/inital

    def volatility(self):
        daily_returns=[]
        for i in range(1,len(self.portfolio_value_history)):
            todaysvalue=self.portfolio_value_history[i]
            yesterday=self.portfolio_value_history[i-1]
            daily_return=(todaysvalue/yesterday)-1
            daily_returns.append(daily_return)
        return numpy.std(daily_returns)