from pyine.indicators import *

# //@version=5
# strategy("Scythe Optimizada con Stop Loss Dinámico", overlay=true, initial_capital=1000)

# // Parámetros de rango de fechas usando input.time()
startDate = input.time(timestamp("2020-01-01"), "Fecha de Inicio", confirm=True)
finishDate = input.time(timestamp("2025-12-31"), "Fecha de Fin", confirm=True)
time_cond = time >= startDate and time <= finishDate

# // Parámetros RSI
rsiLength = input.int(14, "Longitud RSI")
rsiOversold = input.int(30, "Nivel RSI Sobrevendido")
rsiOverbought = input.int(70, "Nivel RSI Sobrecomprado")

# // Calcular RSI
rsi = ta.rsi(close, rsiLength)

# // Condiciones simplificadas para prueba
longCondition = rsi < rsiOversold and time_cond
shortCondition = rsi > rsiOverbought and time_cond

# // Entradas y salidas simplificadas
if longCondition :
#     strategy.entry("Long", strategy.long)

if shortCondition :
#     strategy.entry("Short", strategy.short)

# // Plotear RSI
# plot(rsi, color=color.blue) 