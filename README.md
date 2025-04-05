# Pine Script to Python - Converter and Backtesting

This project allows you to convert trading strategies written in Pine Script (TradingView) to Python, and execute them with real historical data from Binance.

## Configuration

1. Install the necessary dependencies:

```bash
pip install python-binance pandas numpy matplotlib python-dotenv
```

2. Create a `.env` file in the project root with your Binance credentials:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

You can obtain your API keys by creating a Binance account and generating an API key in your profile.

## Basic Usage

### Convert a Pine Script to Python

```bash
python main.py path/to/your_script.pine
```

This will generate a Python file with the script conversion.

### Run the strategy with historical data

```bash
python complete_example.py --symbol BTCUSDT --timeframe 1d --start_date 2022-01-01 --end_date 2023-01-01
```

## Command Line Options

Available options:
- `--symbol`: Trading pair (default: BTCUSDT)
- `--timeframe`: Time interval (1m, 5m, 15m, 1h, 4h, 1d, etc.) (default: 1d)
- `--start_date`: Start date in YYYY-MM-DD format (default: 2022-01-01)
- `--end_date`: End date in YYYY-MM-DD format (default: 2022-12-31)
- `--random`: Use random data instead of Binance data

## Examples

### Convert the Scythe Optimized Strategy

```bash
python main.py ../scripts/scythe_optimizada.pine
```

### Test with Random Data (No Binance API Required)

```bash
python complete_example.py --random
```

### Test with Basic Example (Simplified RSI Strategy)

```bash
python basic_example.py
```

### Test with Real Binance Data for Ethereum

```bash
python complete_example.py --symbol ETHUSDT --timeframe 1d --start_date 2022-01-01 --end_date 2023-01-01
```

### Test with Shorter Timeframes

```bash
python complete_example.py --symbol BTCUSDT --timeframe 4h --start_date 2023-01-01 --end_date 2023-01-31
```

### Test with Very Short Timeframe (Intraday)

```bash
python complete_example.py --symbol BTCUSDT --timeframe 15m --start_date 2023-01-01 --end_date 2023-01-05
```

## Project Structure

- `main.py`: Main script for converting Pine Script to Python
- `complete_example.py`: Complete usage example with historical data
- `basic_example.py`: Simplified example with basic RSI strategy
- `pyine/`: Module with functions and indicators to emulate Pine Script
- `scythe_config.py`: Scythe strategy configuration
- `config.py`: General project configuration
- `.env`: File with credentials (not included in the repository)

## Binance API Documentation

- [Python Binance Documentation](https://python-binance.readthedocs.io/en/latest/)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)

## Supported Features

- Technical indicators (RSI, EMA, SMA, etc.)
- Entry/exit conditions based on indicators
- Backtesting with real historical data
- Results visualization with charts

## Limitations

- Not all Pine Script functions are implemented
- Execution may be slower than in TradingView
- Some complex functions may require manual adjustments

## Next Steps

- Add more technical indicators
- Improve the user interface
- Implement parameter optimization
- Create a web interface to visualize results 