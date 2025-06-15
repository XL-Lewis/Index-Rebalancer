#!/usr/bin/env python3
"""
Demo script showing index rebalancing functionality using the provided sample data.

This script demonstrates:
1. Index construction for the first date (8/04/2025)
2. Index rebalancing for the second date (8/05/2025)
3. Analysis of portfolio changes
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from index_rebalancer import RawData, Index

def main():
    print("=== Index Rebalancer Demo ===\n")
    
    # Load the provided sample data
    print("Loading data from provided_sample.csv...")
    raw_data = RawData("data/provided_sample.csv")
    print(f"Loaded {len(raw_data.data)} rows of data\n")
    
    # Initial index construction (2025-04-08)
    print("1. INITIAL INDEX CONSTRUCTION (8/04/2025)")
    print("-" * 50)
    
    initial_date = "8/04/2025"
    percentile = 0.85  # Top 85% by market cap
    capital = 100_000_000  # $100 million
    
    initial_index = Index(raw_data, initial_date, percentile, capital)
    
    print(f"Date: {initial_date}")
    print(f"Percentile cutoff: {percentile * 100}%")
    print(f"Total capital: ${capital:,}")
    print(f"Number of stocks selected: {len(initial_index.data)}")
    print(f"Total portfolio value: ${initial_index.value():,.2f}")
    
    print("\nSelected stocks:")
    for _, row in initial_index.data.iterrows():
        print(f"  {row['company']}: {row['num_shares_purchased']:.0f} shares @ ${row['price']:.2f} = ${row['allocation']:,.2f}")
    
    # Rebalancing (2025-05-08)
    print("\n\n2. REBALANCING (8/05/2025)")
    print("-" * 50)
    
    rebalance_date = "8/05/2025"
    new_index = Index(raw_data, rebalance_date, percentile, capital)
    
    print(f"New date: {rebalance_date}")
    print(f"Number of stocks in new index: {len(new_index.data)}")
    
    # Calculate portfolio value at new prices before rebalancing
    old_portfolio_value = 0
    print("\nOld portfolio value at new prices:")
    for _, row in initial_index.data.iterrows():
        company = row['company']
        shares = row['num_shares_purchased']
        # Find new price for this company
        new_price_data = raw_data.data[(raw_data.data['date'] == rebalance_date) & 
                                      (raw_data.data['company'] == company)]
        if not new_price_data.empty:
            new_price = new_price_data.iloc[0]['price']
            value = shares * new_price
            old_portfolio_value += value
            print(f"  {company}: {shares:.0f} shares @ ${new_price:.2f} = ${value:,.2f}")
        else:
            print(f"  {company}: No data available for {rebalance_date}")
    
    print(f"\nTotal old portfolio value at new prices: ${old_portfolio_value:,.2f}")
    
    # Perform rebalancing
    rebalance_result = initial_index.rebalance(new_index)
    
    print(f"\n3. REBALANCING TRANSACTIONS")
    print("-" * 50)
    
    total_buy_value = 0
    total_sell_value = 0
    
    for company, change in rebalance_result.items():
        if abs(change) > 0.001:  # Only show meaningful changes
            # Get the price for this company on the rebalance date
            price_data = raw_data.data[(raw_data.data['date'] == rebalance_date) & 
                                      (raw_data.data['company'] == company)]
            if not price_data.empty:
                price = price_data.iloc[0]['price']
                value = abs(change) * price
                action = "BUY" if change > 0 else "SELL"
                print(f"  {action} {company}: {abs(change):.0f} shares @ ${price:.2f} = ${value:,.2f}")
                
                if change > 0:
                    total_buy_value += value
                else:
                    total_sell_value += value
    
    print(f"\nTotal value bought: ${total_buy_value:,.2f}")
    print(f"Total value sold: ${total_sell_value:,.2f}")
    print(f"Net change: ${total_buy_value - total_sell_value:,.2f}")
    
    print(f"\n4. FINAL PORTFOLIO")
    print("-" * 50)
    print(f"Final portfolio value: ${initial_index.value():,.2f}")
    
    print("\nFinal holdings:")
    for _, row in initial_index.data.iterrows():
        print(f"  {row['company']}: {row['num_shares_purchased']:.0f} shares @ ${row['price']:.2f} = ${row['allocation']:,.2f}")

if __name__ == "__main__":
    main()