import pandas as pd

# Raw data read in from a CSV - does some basic sanitization
class RawData:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        # todo: Sanitize inputs

    # Return dataframe, sorted by market cap
    def get_dated_list(self, target_date):
        dated_list = self.data[self.data['date'] == target_date].copy()
        return dated_list.sort_values('market_cap_m', ascending=False).reset_index(drop=True)

    # Returns market cap of stocks on a specific date
    def get_dated_market_cap(self, date):
        return self.get_dated_list(date)['market_cap_m'].sum()


# Balanced stock list
class Index:
    # stock list as RawData
    # date as dd/mm/yyyy
    # percentile as decimal
    def __init__(self, stock_list, date, percentile, capital):

        total_market_cap = stock_list.get_dated_market_cap(date)
        df = stock_list.get_dated_list(date).copy()

        df['weight'] = df['market_cap_m'] / total_market_cap # Calc weights
        df['cumulative_weight'] = df['weight'].cumsum() # Calc cumulative weights
        self.data = df[df['cumulative_weight'] <= percentile].copy() # Filter out percentile
        self.data['weight'] = self.data['market_cap_m'] / self.data['market_cap_m'].sum() # Recalc weights on sub-list
        self.data['allocation'] = self.data['weight'] * capital
        # TODO: Handle fractional shares - currently calculates fractional shares but doesn't
        # decide whether to round up/down when actual share purchases must be whole numbers
        # Example: $5000 allocation / $2501 price = 1.998 shares, but can only buy 1 or 2
        self.data['num_shares_purchased'] = self.data['allocation'] / self.data['price']

    def rebalance(self, new_index):
        old_index = self.data
        


        for row in old_index:
            
        # Compare current index to new index
        # 1. Add stocks are in the new index but not old
        # 2. Remove stocks are in old but not new
        # Do we need to re-adjust weights?
        # return list of sold and purchased stocks
        # test - calculate value of sold/bought stocks and compare to (new index value - old index value)
        pass
    
    def value(self):
        # return the total value of the portfolio
        return (self.data['num_shares_purchased'] * self.data['price']).sum()

