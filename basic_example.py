import pandas as pd
import matplotlib.pyplot as plt
from pyine.indicators import *
import scythe_config as strategy

# Function to load test data
def load_test_data():
    """Load test data or generate random data if none available"""
    try:
        # Try to load real data if available
        df = pd.read_csv('sample_data.csv')
        return df
    except:
        # Generate synthetic data
        print("Generating random test data...")
        dates = pd.date_range(start='2022-01-01', periods=200, freq='D')
        
        # Generate prices with some volatility
        np.random.seed(42)
        close = np.random.normal(100, 10, 200).cumsum() + 500
        
        # Ensure prices are not negative
        close = np.maximum(close, 1)
        
        # Generate OHLC from closing prices
        high = close + np.random.normal(0, 5, 200)
        low = close - np.random.normal(0, 5, 200)
        open_price = low + np.random.random(200) * (high - low)
        
        # Ensure high ≥ open, close ≥ low
        high = np.maximum(high, np.maximum(open_price, close))
        low = np.minimum(low, np.minimum(open_price, close))
        
        # Generate volume
        volume = np.random.normal(1000000, 500000, 200)
        volume = np.maximum(volume, 100)  # Ensure positive volume
        
        df = pd.DataFrame({
            'date': dates,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
        
        return df

# Function to run the strategy
def run_strategy(data):
    """Run the converted strategy on the provided data"""
    # Prepare lists to store signals
    buy_signals = []
    sell_signals = []
    
    # Iterate through the data bar by bar
    for i in range(len(data)):
        if i < 14:  # We need at least 14 bars for RSI
            continue
            
        # Update global variables with the data for this bar
        update_ohlcv(
            data['open'].iloc[i],
            data['high'].iloc[i],
            data['low'].iloc[i],
            data['close'].iloc[i],
            data['volume'].iloc[i]
        )
        
        # Calculate RSI with the data up to this bar
        rsi_value = calculate_rsi(data['close'].iloc[:i+1], strategy.rsiLength)
        
        # Check entry conditions
        if rsi_value < strategy.rsiOversold:
            print(f"Buy signal at {data['date'].iloc[i]}, RSI: {rsi_value:.2f}")
            buy_signals.append(i)
        
        if rsi_value > strategy.rsiOverbought:
            print(f"Sell signal at {data['date'].iloc[i]}, RSI: {rsi_value:.2f}")
            sell_signals.append(i)
    
    return buy_signals, sell_signals

# Function to plot results
def plot_results(data, buy_signals, sell_signals):
    """Plot prices with buy/sell signals"""
    plt.figure(figsize=(12, 8))
    
    # Plot closing price
    plt.plot(data['close'], label='Closing price')
    
    # Plot buy and sell signals
    for buy in buy_signals:
        plt.scatter(buy, data['close'].iloc[buy], color='green', marker='^', s=100)
    
    for sell in sell_signals:
        plt.scatter(sell, data['close'].iloc[sell], color='red', marker='v', s=100)
    
    plt.title('Basic RSI Strategy Example')
    plt.xlabel('Bars')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main function
def main():
    print("Running basic Pine Script to Python conversion example")
    
    # Load data
    data = load_test_data()
    print(f"Data loaded: {len(data)} records")
    
    # Run strategy
    buy_signals, sell_signals = run_strategy(data)
    
    # Show results
    print(f"Total buy signals: {len(buy_signals)}")
    print(f"Total sell signals: {len(sell_signals)}")
    
    # Plot results
    plot_results(data, buy_signals, sell_signals)

if __name__ == "__main__":
    main() 