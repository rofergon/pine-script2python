import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyine.indicators import *
import argparse
import sys
import os

# Import configuration and data provider
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import DEFAULT_SYMBOL, DEFAULT_TIMEFRAME, DEFAULT_START_DATE, DEFAULT_END_DATE
from pyine.data_provider import get_historical_data

# Implement necessary TradingView functions
def ta_lowest(source, length):
    """Simplified implementation of ta.lowest"""
    if isinstance(source, (int, float)):
        return source  # If it's a single value, we return it
    # If it's a series, we return the minimum of the last 'length' values
    if isinstance(source, pd.Series):
        return source.rolling(window=length).min().iloc[-1]
    # If it's a list, we calculate the minimum of the last 'length' elements
    return min(source[-length:]) if len(source) >= length else None

def ta_highest(source, length):
    """Simplified implementation of ta.highest"""
    if isinstance(source, (int, float)):
        return source  # If it's a single value, we return it
    # If it's a series, we return the maximum of the last 'length' values
    if isinstance(source, pd.Series):
        return source.rolling(window=length).max().iloc[-1]
    # If it's a list, we calculate the maximum of the last 'length' elements
    return max(source[-length:]) if len(source) >= length else None

def ta_crossover(a, b):
    """Implementation of ta.crossover: a crosses above b"""
    # Needs history, for simplicity we assume a and b are Series
    if len(a) < 2 or len(b) < 2:
        return False
    return a.iloc[-2] < b.iloc[-2] and a.iloc[-1] > b.iloc[-1]

def ta_crossunder(a, b):
    """Implementation of ta.crossunder: a crosses below b"""
    # Needs history, for simplicity we assume a and b are Series
    if len(a) < 2 or len(b) < 2:
        return False
    return a.iloc[-2] > b.iloc[-2] and a.iloc[-1] < b.iloc[-1]

# Add to the indicators module
ta = type('ta', (), {
    'lowest': ta_lowest,
    'highest': ta_highest,
    'crossover': ta_crossover,
    'crossunder': ta_crossunder
})

math = type('math', (), {
    'abs': abs
})

# Import the converted strategy
import scythe_config as strategy

# Function to load historical data
def load_historical_data(symbol, timeframe, start_date, end_date, use_binance=True):
    """Load historical data from Binance or generate random data"""
    provider_type = 'binance' if use_binance else 'random'
    try:
        return get_historical_data(
            symbol=symbol,
            interval=timeframe,
            start_date=start_date,
            end_date=end_date,
            provider_type=provider_type
        )
    except Exception as e:
        print(f"Error loading historical data: {e}")
        print("Generating random data...")
        from pyine.data_provider import DataProvider
        return DataProvider().generate_random_data()

# Function to run the strategy
def run_strategy(data):
    """Run the converted strategy on the provided data"""
    # Prepare lists to store signals
    buy_signals = []
    sell_signals = []
    
    # Define variables for calculations
    emas = {}  # Dictionary to store EMAs
    
    # Iterate through the data bar by bar (as Pine Script would)
    for i in range(len(data)):
        if i < 50:  # We need at least 50 bars for indicators
            continue
            
        # Update global variables with the data for this bar
        strategy.close = data['close'].iloc[i]
        strategy.high = data['high'].iloc[i]
        strategy.low = data['low'].iloc[i]
        strategy.open = data['open'].iloc[i]
        strategy.volume = data['volume'].iloc[i]
        
        # Also update those from the indicators module
        update_ohlcv(
            data['open'].iloc[i],
            data['high'].iloc[i],
            data['low'].iloc[i],
            data['close'].iloc[i],
            data['volume'].iloc[i]
        )
        
        # Access to historical data
        close_history = data['close'].iloc[:i+1]
        high_history = data['high'].iloc[:i+1]
        low_history = data['low'].iloc[:i+1]
        volume_history = data['volume'].iloc[:i+1]
        
        # Calculate RSI
        rsi_value = calculate_rsi(close_history, strategy.rsiLength)
        
        # Simplified conditions for testing
        # We only use RSI to generate example signals
        if rsi_value < strategy.rsiOversold:
            print(f"Buy signal at {data['date'].iloc[i]}, RSI: {rsi_value:.2f}")
            buy_signals.append(i)
        
        if rsi_value > strategy.rsiOverbought:
            print(f"Sell signal at {data['date'].iloc[i]}, RSI: {rsi_value:.2f}")
            sell_signals.append(i)
    
    return buy_signals, sell_signals

# Function to plot results
def plot_results(data, buy_signals, sell_signals, symbol):
    """Plot prices with buy/sell signals"""
    plt.figure(figsize=(12, 8))
    
    # Plot closing price
    plt.plot(data['date'], data['close'], label='Closing price')
    
    # Plot buy and sell signals
    for buy in buy_signals:
        plt.scatter(data['date'].iloc[buy], data['close'].iloc[buy], color='green', marker='^', s=100)
    
    for sell in sell_signals:
        plt.scatter(data['date'].iloc[sell], data['close'].iloc[sell], color='red', marker='v', s=100)
    
    plt.title(f'Scythe Optimized Strategy - {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to parse arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Run Scythe strategy with historical data')
    
    parser.add_argument('--symbol', type=str, default=DEFAULT_SYMBOL,
                        help=f'Trading pair (default: {DEFAULT_SYMBOL})')
    
    parser.add_argument('--timeframe', type=str, default=DEFAULT_TIMEFRAME,
                        help=f'Time interval (1m, 5m, 1h, 1d, etc.) (default: {DEFAULT_TIMEFRAME})')
    
    parser.add_argument('--start_date', type=str, default=DEFAULT_START_DATE,
                        help=f'Start date in YYYY-MM-DD format (default: {DEFAULT_START_DATE})')
    
    parser.add_argument('--end_date', type=str, default=DEFAULT_END_DATE,
                        help=f'End date in YYYY-MM-DD format (default: {DEFAULT_END_DATE})')
    
    parser.add_argument('--random', action='store_true',
                        help='Use random data instead of Binance')
    
    return parser.parse_args()

# Main function
def main():
    print("Running the Scythe Optimized strategy converted from Pine Script to Python")
    
    # Parse arguments
    args = parse_arguments()
    
    # Load data
    data = load_historical_data(
        symbol=args.symbol,
        timeframe=args.timeframe,
        start_date=args.start_date,
        end_date=args.end_date,
        use_binance=not args.random
    )
    
    print(f"Data loaded: {len(data)} records")
    
    # Run strategy
    buy_signals, sell_signals = run_strategy(data)
    
    # Show results
    print(f"Total buy signals: {len(buy_signals)}")
    print(f"Total sell signals: {len(sell_signals)}")
    
    # Plot results
    plot_results(data, buy_signals, sell_signals, args.symbol)

if __name__ == "__main__":
    main() 