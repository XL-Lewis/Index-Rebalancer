import pandas as pd

class RawData:
    """CSV stock data reader with some basic validation."""
    
    def __init__(self, file_path: str) -> None:
        """Load and validate CSV stock data."""
        try:
            self.data = pd.read_csv(file_path)
            self._validate_data()
        except FileNotFoundError:
            raise ValueError(f"CSV file not found: {file_path}")
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file is empty: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading CSV file {file_path}: {str(e)}")
    
    def _validate_data(self) -> None:
        """Validate required columns and data integrity."""
        required_columns = ['date', 'company', 'market_cap_m', 'price']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for null values in critical columns
        for col in required_columns:
            if self.data[col].isnull().any():
                raise ValueError(f"Null values found in column: {col}")
        
        # Check for negative values in financial columns
        if (self.data['market_cap_m'] < 0).any():
            raise ValueError("Negative market cap values found")
        if (self.data['price'] < 0).any():
            raise ValueError("Negative price values found")

    def get_dated_list(self, target_date: str) -> pd.DataFrame:
        """Get stocks for date, sorted by market cap (descending)."""
        dated_list = self.data[self.data['date'] == target_date].copy()
        return dated_list.sort_values('market_cap_m', ascending=False).reset_index(drop=True)

    def get_dated_market_cap(self, date: str) -> float:
        """Get total market cap for date."""
        return self.get_dated_list(date)['market_cap_m'].sum()


class Index:
    """Market cap weighted index with percentile filtering."""
    
    def __init__(self, stock_list: RawData, date: str, percentile: float, capital: float) -> None:
        """Create index from top percentile stocks by market cap."""
        # Input validation
        if not (0 < percentile <= 1):
            raise ValueError(f"Percentile must be between 0 and 1, got {percentile}")
        if capital <= 0:
            raise ValueError(f"Capital must be positive, got {capital}")

        total_market_cap = stock_list.get_dated_market_cap(date)
        if total_market_cap == 0:
            raise ValueError(f"Total market cap is zero for date {date}")
            
        df = stock_list.get_dated_list(date).copy()
        if len(df) == 0:
            raise ValueError(f"No data found for date {date}")

        df['weight'] = df['market_cap_m'] / total_market_cap # Calc weights
        df['cumulative_weight'] = df['weight'].cumsum() # Calc cumulative weights
        self.data = df[df['cumulative_weight'] <= percentile].copy() # Filter out percentile
        
        if len(self.data) == 0:
            raise ValueError(f"No stocks selected with percentile {percentile} for date {date}")
            
        self.data['weight'] = self.data['market_cap_m'] / self.data['market_cap_m'].sum() # Recalc weights on sub-list
        self.data['allocation'] = self.data['weight'] * capital
        self.data['num_shares_purchased'] = self.data['allocation'] / self.data['price']

    def rebalance(self, new_index: 'Index') -> dict[str, float]:
        """Rebalance to match new_index. Returns {company: change_in_shares}."""
        # Use pandas merge to combine old and new holdings
        old_holdings = self.data[['company', 'num_shares_purchased']].copy()
        old_holdings.columns = ['company', 'old_shares']
        
        new_holdings = new_index.data[['company', 'num_shares_purchased']].copy()
        new_holdings.columns = ['company', 'new_shares']
        
        # Merge on company, filling missing values with 0
        merged = pd.merge(old_holdings, new_holdings, on='company', how='outer').fillna(0)
        
        # Calculate change in shares for each company
        merged['change_in_shares'] = merged['new_shares'] - merged['old_shares']
        
        # Convert to dictionary format {company: change_in_shares}
        rebalance_dict = merged.set_index('company')['change_in_shares'].to_dict()
        
        # Update current index data to match new index
        self.data = new_index.data.copy()
        
        return rebalance_dict
    
    def value(self) -> float:
        """Return total portfolio value."""
        return (self.data['num_shares_purchased'] * self.data['price']).sum()

