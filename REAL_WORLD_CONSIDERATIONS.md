# Things that I've handled in code 
- Basic validation for 
    - CSV file (CSV missing / empty etc.)
    - CSV data (negative / null values etc.)
    - Request errors (Bad allocation / percentile)

# Things I've thought about (but not handled):
- Fractional shares
    At the moment, we allow shares with decimal points, where realistically, it is impossible to buy '0.5' shares. This requires a more complex implementation to handle. 
- Numerical accuracy / reproducibility
    We want the numbers to be reproducible, with a high degree of accuracy. I assume pandas has some way of managing this, but I noticed while testing that we had to round some of the values. We don't specify any constraints around rounding at the moment.
- Handling bad data
    - Bad dates
    - Data duplication
    - Bad formatting
    - Sanity checks (i.e. one share erroneously is >99.9% of index)
    - Divide by 0 errors
    - Bad function inputs (i.e. percentile > 0)
- Time
    Prices move in realtime, and may change between calculation and actual purchase (or even during the running of the program)
- Volume movements / liquidity
    Index rebalancing (depending on the size of the index) can result in significant numbers of shares being purchased, which may change the share value
- General market movements
    Markets also do things like stock splits, dividends, buy backs etc.
- Cost of rebalancing
    - Transaction fees
    - Purchase fees
    - Currency conversion
- Tax
    Very simple and easy to manage I'm sure /s
- Testing
    Currently fairly simple - doesn't cover many edge cases

# Identifying errors

To help fix and identify errors, it would be worth including the following

- Structured logging
    - Include data values at each transformation step
- Comprehensive unit tests, including edge cases and integration testing
- Validation
    - Input validation for items passed in
    - Output validation
- Clear documentation including
    - Assumptions
    - Any known sources of errors or gaps in implementation
    - A design doc with an overview of the brief and breakdown 




