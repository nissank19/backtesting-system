class Backtester:
    def runback(self,df,inital=1000,share=0):
        self.portfolio_value_history = []
        self.cash=inital
        self.share=share
        for index, row in df.iterrows():
            if row["signal"]==1:
                self.buy(row["adj_close"])
                self.portfolio_value_history.append((self.cash,self.share*row["adj_close"]))
            elif row["signal"]==-1:
                self.sell(row["adj_close"])
                self.portfolio_value_history((self.cash, self.share*row["adj_close"]))
            else: print("hold")





    def buy(self,price):
        if self.cash<=0:
            print("no cash")
            return
        else:
         sharestobuy=self.cash/price
         self.cash=0
         self.share+=sharestobuy
    def sell(self,price):
        if self.share==0:
            print('no shares')
        else:
            sharstosellprice=self.share*price
            self.cash+=sharstosellprice
            self.share=0