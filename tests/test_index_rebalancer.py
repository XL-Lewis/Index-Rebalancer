# NOTE - Tests have been (mostly) LLM generated from test definitions.

import pytest
import pandas as pd
import sys
import os

# Add src directory to path so we can import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from index_rebalancer import RawData, Index


class TestRawData:

    def test_import(self):
        raw_data = RawData("tests/fixtures/simple.csv")
        assert raw_data.data is not None
        assert len(raw_data.data) > 0

    def test_get_dated_list_returns_sorted_by_market_cap(self):
        """Test that get_dated_list returns data for specific date sorted by market cap descending"""
        raw_data = RawData("tests/fixtures/simple.csv")
        
        # Get data for 2/01/2025 - should have B(20), A(10), C(10), E(10), D(5)
        dated_list = raw_data.get_dated_list("2/01/2025")
        
        # Should return 5 companies for that date
        assert len(dated_list) == 5
        
        # Should be sorted by market_cap_m descending
        market_caps = dated_list['market_cap_m'].tolist()
        assert market_caps == [20, 10, 10, 10, 5]
        
        # First company should be B (highest market cap)
        assert dated_list.iloc[0]['company'] == 'B'
        assert dated_list.iloc[0]['market_cap_m'] == 20

    def test_get_dated_market_cap_sums_correctly(self):
        """Test that get_dated_market_cap returns correct sum for a specific date"""
        raw_data = RawData("tests/fixtures/simple.csv")
        
        # Test for 1/01/2025 - all companies have 10M market cap
        total_market_cap = raw_data.get_dated_market_cap("1/01/2025")
        assert total_market_cap == 50  # 5 companies * 10M each
        
        # Test for 2/01/2025 - B=20, A=10, C=10, E=10, D=5
        total_market_cap = raw_data.get_dated_market_cap("2/01/2025")
        assert total_market_cap == 55  # 20+10+10+10+5


class TestIndex:

    def test_index_initialization_with_percentile_filtering(self):
        """Test that Index correctly initializes with percentile filtering"""
        raw_data = RawData("tests/fixtures/simple.csv")
        
        # Create index with top 60% of companies by market cap for 2/01/2025
        # Market caps: B(20), A(10), C(10), E(10), D(5) - top 60% should be B, A, C
        index = Index(raw_data, "2/01/2025", .85, 100_000)
        
        # Should contain top 85% of stocks (3 out of 5)
        assert len(index.data) == 3
        
        # Should include the top market cap companies
        stock_companies = index.data['company'].tolist()
        assert 'B' in stock_companies  # Highest market cap
        assert 'A' in stock_companies  # Second highest
        assert 'C' in stock_companies  # Third highest (tied with E, but should be included)

        # Note - we're not really dealing with precision properly here.
        # Ideally, we'd be using a library that handles calculations exactly
        assert index.value() == pytest.approx(100_000)

        # Retry same as above with diff percentile
        raw_data = RawData("tests/fixtures/simple.csv")
        index = Index(raw_data, "2/01/2025", .65, 100_000)
        
        # Should contain top 65% of stocks (2 out of 5)
        assert len(index.data) == 2
        
        # Should include the top market cap companies
        stock_companies = index.data['company'].tolist()
        assert 'B' in stock_companies  # Highest market cap
        assert 'A' in stock_companies  # Second highest

        assert index.value() == pytest.approx(100_000)


    def test_index_rebalance_identifies_changes(self):
        """Test that rebalance method identifies stocks to buy/sell"""
        raw_data = RawData("tests/fixtures/simple.csv")
        
        # Create old index (1/01/2025) and new index (2/01/2025)
        old_index = Index(raw_data, "1/01/2025", 80, 100_000)  # Top 80% of stocks
        new_index = Index(raw_data, "2/01/2025", 80, 100_000)  # Top 80% of stocks
        
        # Rebalance from old to new
        rebalance_result = old_index.rebalance(new_index)
        
        # Should return some structure indicating changes
        assert rebalance_result is not None
        
        # Should have information about stocks to buy/sell
        assert hasattr(rebalance_result, '__iter__') or isinstance(rebalance_result, dict)


if __name__ == "__main__":
    pytest.main([__file__])