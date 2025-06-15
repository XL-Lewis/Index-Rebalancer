# Index Rebalancer

A Python implementation of market cap weighted index fund construction and rebalancing functionality.

## Disclaimer and preface

LLMs have been used to generate some parts of the testing, docs, and the demo file. The module code is handwritten.

I've taken this as an opportunity to start learning pandas, so I've spent a bit more than the suggested '90 minute' timeframe. 

## Overview

This project implements a market cap weighted index fund that can:
1. Construct an initial index based on market capitalization percentiles
2. Rebalance the index when market conditions change
3. Calculate buy/sell transactions when rebalancing 

## Installation

You will need Poetry to run this project. 

To set up:

```bash
# Install dependencies
poetry install

# Run commands (Poetry automatically uses the virtual environment)
poetry run python demo.py
```

## Usage

### Basic Usage

```python
from src.index_rebalancer import RawData, Index

# Load data
raw_data = RawData("data/provided_sample.csv")

# Create initial index (85th percentile, $100M capital)
initial_index = Index(raw_data, "8/04/2025", 0.85, 100_000_000)

# Create new index for rebalancing
new_index = Index(raw_data, "8/05/2025", 0.85, 100_000_000)

# Rebalance
changes = initial_index.rebalance(new_index)
print(changes)  # {company: change_in_shares}
```

### Demo Script

Run the included demo to see the rebalancer in action:

```bash
poetry run python demo.py
```

This demonstrates:
- Initial index construction for 8/04/2025
- Portfolio valuation at new prices on 8/05/2025
- Rebalancing transactions required
- Final portfolio composition

## Running Tests

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_index_rebalancer.py -v
```
