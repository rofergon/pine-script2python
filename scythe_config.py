"""
Simplified configuration for testing the Scythe strategy
"""

# RSI parameters
rsiLength = 14
rsiOversold = 45
rsiOverbought = 55

# Dynamic stop loss parameter
stopLossPercent = 2.0

# Improved short entry parameters
maxDistancePercent = 1.0
volumeMultiplier = 1.0

# Support and resistance line parameters
# Support line 1
emaSupp1Length = 20
emaSupp1Lookback = 50
emaSupp1Source = "low"

# Support line 2
emaSupp2Length = 3
emaSupp2Lookback = 50
emaSupp2Source = "low"

# Resistance line 1
emaRes1Length = 50
emaRes1Lookback = 50
emaRes1Source = "high"

# Resistance line 2
emaRes2Length = 100
emaRes2Lookback = 50
emaRes2Source = "high"

# Selling pressure condition
hasSellingPressure = True

# Function to get the correct data source
def getSource(src):
    """Convert Pine Script source to Python data source"""
    if src == "close":
        return close
    elif src == "high":
        return high
    elif src == "low":
        return low
    elif src == "open":
        return open
    return close  # Default to close

# Global variables for OHLCV data
close = 0
high = 0
low = 0
open = 0
volume = 0 