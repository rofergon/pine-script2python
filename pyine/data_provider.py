import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import requests
from binance.client import Client
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BINANCE_API_KEY, BINANCE_API_SECRET, DEFAULT_SYMBOL, DEFAULT_TIMEFRAME

class DataProvider:
    """Base class for data providers"""
    
    def get_historical_data(self, symbol, interval, start_date, end_date):
        """Method to be implemented by child classes"""
        pass
        
    def generate_random_data(self, periods=200):
        """Generate random data for testing"""
        dates = pd.date_range(start='2022-01-01', periods=periods, freq='D')
        
        # Generate realistic prices with more volatility
        np.random.seed(42)
        close = np.random.normal(100, 30, periods).cumsum() + 500
        
        # Ensure prices are not negative
        close = np.maximum(close, 1)
        
        # Generate OHLC from closing prices
        high = close + np.random.normal(0, 20, periods)
        low = close - np.random.normal(0, 20, periods)
        open_price = low + np.random.random(periods) * (high - low)
        
        # Ensure that high ≥ open, close ≥ low
        high = np.maximum(high, np.maximum(open_price, close))
        low = np.minimum(low, np.minimum(open_price, close))
        
        # Generate volume
        volume = np.random.normal(1000000, 500000, periods)
        volume = np.maximum(volume, 100)
        
        df = pd.DataFrame({
            'date': dates,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
        
        return df


class BinanceDataProvider(DataProvider):
    """Provider for historical data from Binance"""
    
    def __init__(self, api_key=None, api_secret=None):
        """Initialize Binance client with API keys"""
        self.api_key = api_key or BINANCE_API_KEY
        self.api_secret = api_secret or BINANCE_API_SECRET
        
        # Check if keys are configured
        if not self.api_key or not self.api_secret:
            print("WARNING: Binance API keys not configured.")
            print("Please create a .env file with BINANCE_API_KEY and BINANCE_API_SECRET.")
            self.client = None
        else:
            try:
                self.client = Client(self.api_key, self.api_secret)
                print("Binance client initialized successfully.")
            except Exception as e:
                print(f"Error initializing Binance client: {e}")
                self.client = None
    
    def get_historical_data(self, symbol=DEFAULT_SYMBOL, interval=DEFAULT_TIMEFRAME, 
                           start_date=None, end_date=None):
        """
        Get historical data from Binance
        
        Args:
            symbol (str): Trading pair (e.g. 'BTCUSDT')
            interval (str): Time interval ('1m', '1h', '1d', etc.)
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            
        Returns:
            DataFrame: OHLCV data with columns 'date', 'open', 'high', 'low', 'close', 'volume'
        """
        if not self.client:
            print("No Binance client available. Generating random data...")
            return self.generate_random_data()
        
        try:
            # Convert dates to timestamp in milliseconds
            if start_date:
                start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)
            else:
                # Default to 1 year ago
                start_ts = int((datetime.now() - timedelta(days=365)).timestamp() * 1000)
                
            if end_date:
                end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp() * 1000)
            else:
                end_ts = int(datetime.now().timestamp() * 1000)
            
            print(f"Getting historical data for {symbol} at {interval} from {start_date} to {end_date}...")
            
            # Get historical data
            klines = self.client.get_historical_klines(
                symbol=symbol,
                interval=interval,
                start_str=start_ts,
                end_str=end_ts
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Convert data types
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
                
            # Select and reorder columns
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
            
            print(f"Data retrieved: {len(df)} records")
            return df
            
        except Exception as e:
            print(f"Error getting data from Binance: {e}")
            print("Generating random data as fallback...")
            return self.generate_random_data()


def get_data_provider(provider_type='binance'):
    """
    Factory to get the appropriate data provider
    
    Args:
        provider_type (str): Provider type ('binance', 'random')
        
    Returns:
        DataProvider: Instance of the data provider
    """
    if provider_type.lower() == 'binance':
        return BinanceDataProvider()
    else:
        return DataProvider()  # Returns the basic provider (random data)


# Function for simple usage
def get_historical_data(symbol=DEFAULT_SYMBOL, interval=DEFAULT_TIMEFRAME, 
                        start_date=None, end_date=None, provider_type='binance'):
    """
    Get historical data from the selected provider
    
    Args:
        symbol (str): Trading pair (e.g. 'BTCUSDT')
        interval (str): Time interval ('1m', '1h', '1d', etc.)
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        provider_type (str): Provider type ('binance', 'random')
        
    Returns:
        DataFrame: OHLCV data
    """
    provider = get_data_provider(provider_type)
    return provider.get_historical_data(symbol, interval, start_date, end_date) 