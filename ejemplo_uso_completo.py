import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyine.indicators import *

# Implementar funciones necesarias de TradingView
def ta_lowest(source, length):
    """Implementación simplificada de ta.lowest"""
    if isinstance(source, (int, float)):
        return source  # Si es un solo valor, lo devolvemos
    # Si es una serie, devolvemos el mínimo de los últimos 'length' valores
    if isinstance(source, pd.Series):
        return source.rolling(window=length).min().iloc[-1]
    # Si es una lista, calculamos el mínimo de los últimos 'length' elementos
    return min(source[-length:]) if len(source) >= length else None

def ta_highest(source, length):
    """Implementación simplificada de ta.highest"""
    if isinstance(source, (int, float)):
        return source  # Si es un solo valor, lo devolvemos
    # Si es una serie, devolvemos el máximo de los últimos 'length' valores
    if isinstance(source, pd.Series):
        return source.rolling(window=length).max().iloc[-1]
    # Si es una lista, calculamos el máximo de los últimos 'length' elementos
    return max(source[-length:]) if len(source) >= length else None

def ta_crossover(a, b):
    """Implementación de ta.crossover: a cruza por encima de b"""
    # Necesita historiales, para simplificar asumimos que a y b son Series
    if len(a) < 2 or len(b) < 2:
        return False
    return a.iloc[-2] < b.iloc[-2] and a.iloc[-1] > b.iloc[-1]

def ta_crossunder(a, b):
    """Implementación de ta.crossunder: a cruza por debajo de b"""
    # Necesita historiales, para simplificar asumimos que a y b son Series
    if len(a) < 2 or len(b) < 2:
        return False
    return a.iloc[-2] > b.iloc[-2] and a.iloc[-1] < b.iloc[-1]

# Añadir al módulo indicators
ta = type('ta', (), {
    'lowest': ta_lowest,
    'highest': ta_highest,
    'crossover': ta_crossover,
    'crossunder': ta_crossunder
})

math = type('math', (), {
    'abs': abs
})

# Importar la estrategia convertida
import scythe_config as strategy

# Función para inicializar datos de prueba
def load_test_data():
    """Carga datos de prueba o usa datos aleatorios si no hay disponibles"""
    try:
        # Intentar cargar datos reales si están disponibles
        df = pd.read_csv('sample_data.csv')
        return df
    except:
        # Generar datos sintéticos
        print("Generando datos de prueba aleatorios...")
        dates = pd.date_range(start='2022-01-01', periods=200, freq='D')
        
        # Generar precios realistas con más volatilidad
        np.random.seed(42)
        close = np.random.normal(100, 30, 200).cumsum() + 500  # Mayor volatilidad
        
        # Asegurar que los precios no sean negativos
        close = np.maximum(close, 1)
        
        # Generar OHLC a partir de los precios de cierre
        high = close + np.random.normal(0, 20, 200)  # Mayor rango
        low = close - np.random.normal(0, 20, 200)   # Mayor rango
        open_price = low + np.random.random(200) * (high - low)
        
        # Asegurar que high ≥ open, close ≥ low
        high = np.maximum(high, np.maximum(open_price, close))
        low = np.minimum(low, np.minimum(open_price, close))
        
        # Generar volumen
        volume = np.random.normal(1000000, 500000, 200)
        volume = np.maximum(volume, 100)  # Asegurar volumen positivo
        
        df = pd.DataFrame({
            'date': dates,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
        
        return df

# Función para ejecutar la estrategia
def run_strategy(data):
    """Ejecuta la estrategia convertida en los datos proporcionados"""
    # Preparar listas para almacenar señales
    buy_signals = []
    sell_signals = []
    
    # Definir variables para cálculos
    emas = {}  # Diccionario para almacenar EMAs
    
    # Recorrer los datos barra por barra (como lo haría Pine Script)
    for i in range(len(data)):
        if i < 50:  # Necesitamos al menos 50 barras para indicadores
            continue
            
        # Actualizar variables globales con los datos de esta barra
        strategy.close = data['close'].iloc[i]
        strategy.high = data['high'].iloc[i]
        strategy.low = data['low'].iloc[i]
        strategy.open = data['open'].iloc[i]
        strategy.volume = data['volume'].iloc[i]
        
        # También actualizar las del módulo indicators
        update_ohlcv(
            data['open'].iloc[i],
            data['high'].iloc[i],
            data['low'].iloc[i],
            data['close'].iloc[i],
            data['volume'].iloc[i]
        )
        
        # Acceso a datos históricos
        close_history = data['close'].iloc[:i+1]
        high_history = data['high'].iloc[:i+1]
        low_history = data['low'].iloc[:i+1]
        volume_history = data['volume'].iloc[:i+1]
        
        # Calcular RSI
        rsi_value = calculate_rsi(close_history, strategy.rsiLength)
        
        # Condiciones simplificadas para pruebas
        # Solo usamos RSI para generar señales de ejemplo
        if rsi_value < strategy.rsiOversold:
            print(f"Señal de compra en {data['date'].iloc[i]}, RSI: {rsi_value:.2f}")
            buy_signals.append(i)
        
        if rsi_value > strategy.rsiOverbought:
            print(f"Señal de venta en {data['date'].iloc[i]}, RSI: {rsi_value:.2f}")
            sell_signals.append(i)
    
    return buy_signals, sell_signals

# Función para graficar resultados
def plot_results(data, buy_signals, sell_signals):
    """Grafica los precios con las señales de compra/venta"""
    plt.figure(figsize=(12, 8))
    
    # Graficar precio de cierre
    plt.plot(data['close'], label='Precio de cierre')
    
    # Graficar señales de compra y venta
    for buy in buy_signals:
        plt.scatter(buy, data['close'].iloc[buy], color='green', marker='^', s=100)
    
    for sell in sell_signals:
        plt.scatter(sell, data['close'].iloc[sell], color='red', marker='v', s=100)
    
    plt.title('Estrategia Scythe Optimizada')
    plt.xlabel('Barras')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Función principal
def main():
    print("Ejecutando la estrategia Scythe Optimizada convertida de Pine Script a Python")
    
    # Cargar datos
    data = load_test_data()
    print(f"Datos cargados: {len(data)} registros")
    
    # Ejecutar estrategia
    buy_signals, sell_signals = run_strategy(data)
    
    # Mostrar resultados
    print(f"Total señales de compra: {len(buy_signals)}")
    print(f"Total señales de venta: {len(sell_signals)}")
    
    # Graficar resultados
    plot_results(data, buy_signals, sell_signals)

if __name__ == "__main__":
    main() 