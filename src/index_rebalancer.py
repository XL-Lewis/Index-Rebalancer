import pandas as pd

# Raw data read in from a CSV - does some basic sanitization
class RawData:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        # todo: Sanitize inputs

    def get_dated_list(self, target_date):
        dated_list = self.data[self.data['date'] == target_date].copy()
        return dated_list.sort_values('market_cap_m', ascending=False).reset_index(drop=True)

    # Returns market cap of stocks on a specific date
    def get_dated_market_cap(self, date):
        return self.get_dated_list(date)['market_cap_m'].sum()


# Balanced stock list
class Index:
    def __init__(stock_list, percentile):
        # Filter stocks by percentile, calculate weights

    def rebalance(self, new_index):
        # Compare current index to new index
        # 1. Add stocks are in the new index but not old
        # 2. Remove stocks are in old but not new
        # Do we need to re-adjust weights?
        # return list of sold and purchased stocks
        # test - calculate value of sold/bought stocks and compare to (new index value - old index value)
    
    def value(self): 
        # return the total value of the portfolio

