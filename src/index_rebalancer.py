import pandas

# Raw data read in from a CSV - does some basic sanitization
class RawData:
    def __init__(file_path)
        # Get csv 
        # Sanitize inputs

    def get_dated_list(self, date):
        # Get stocks matching a date

    def get_dated_market_cap(date)
        # Get total market cap of stocks matching a date


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

