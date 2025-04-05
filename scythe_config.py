"""
Configuración simplificada de la estrategia Scythe Optimizada para pruebas
"""

# Parámetros RSI con mayor sensibilidad
rsiLength = 14
rsiOversold = 45  # Valor más alto para capturar más señales
rsiOverbought = 55  # Valor más bajo para capturar más señales

# Parámetros Stop Loss Dinámico
stopLossPercent = 2.0

# Parámetros para entrada en corto mejorada
maxDistancePercent = 1.0  # Mayor tolerancia
volumeMultiplier = 1.0  # Criterio de volumen menos estricto

# Parámetros para las líneas de soporte y resistencia
# Soporte 1
emaSupp1Length = 20
emaSupp1Lookback = 50
emaSupp1Source = "low"

# Soporte 2
emaSupp2Length = 3
emaSupp2Lookback = 50
emaSupp2Source = "low"

# Resistencia 1
emaRes1Length = 50
emaRes1Lookback = 50
emaRes1Source = "high"

# Resistencia 2
emaRes2Length = 100
emaRes2Lookback = 50
emaRes2Source = "high"

# Variables para seguimiento
hasSellingPressure = True  # Por defecto asumimos que hay presión de venta

# Función para obtener la fuente de datos correcta
def getSource(src):
    """Convertido manualmente desde switch de Pine Script"""
    if src == "close":
        return close
    elif src == "high":
        return high
    elif src == "low":
        return low
    elif src == "open":
        return open
    else:
        return None  # Valor por defecto

# Variables globales 
close = 0
high = 0
low = 0
open = 0
volume = 0 