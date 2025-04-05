import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyine.indicators import *

# Importar la estrategia convertida
import scythe_fragment as strategy

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
        dates = pd.date_range(start='2022-01-01', periods=100, freq='D')
        
        # Generar precios realistas
        np.random.seed(42)
        close = np.random.normal(100, 10, 100).cumsum() + 500
        
        # Asegurar que los precios no sean negativos
        close = np.maximum(close, 1)
        
        # Generar OHLC a partir de los precios de cierre
        high = close + np.random.normal(0, 5, 100)
        low = close - np.random.normal(0, 5, 100)
        open_price = low + np.random.random(100) * (high - low)
        
        # Asegurar que high ≥ open, close ≥ low
        high = np.maximum(high, np.maximum(open_price, close))
        low = np.minimum(low, np.minimum(open_price, close))
        
        # Generar volumen
        volume = np.random.normal(1000000, 500000, 100)
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
    
    # Recorrer los datos barra por barra (como lo haría Pine Script)
    for i in range(len(data)):
        if i < 14:  # Necesitamos al menos 14 barras para RSI
            continue
            
        # Actualizar variables globales con los datos de esta barra
        update_ohlcv(
            data['open'].iloc[i],
            data['high'].iloc[i],
            data['low'].iloc[i],
            data['close'].iloc[i],
            data['volume'].iloc[i]
        )
        
        # Calcular RSI con los datos hasta esta barra
        rsi_value = calculate_rsi(data['close'].iloc[:i+1], strategy.rsiLength)
        
        # Verificar condiciones de entrada
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
    plt.figure(figsize=(12, 6))
    
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