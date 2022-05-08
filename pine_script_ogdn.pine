// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © OgdnAmes

//@version=4
strategy(title="HF LONG MACD 3.0 5m",overlay=true, pyramiding=0, default_qty_type= strategy.percent_of_equity, default_qty_value = 100, calc_on_order_fills=false, slippage=1,commission_type=strategy.commission.percent,commission_value=0, process_orders_on_close=false, precision = 16)
///Inputs Here

fast_length = input(title="Fast Length", type=input.integer, defval=12, minval = 1)
slow_length = input(title="Slow Length", type=input.integer, defval=26, minval = 1)
src = input(title="Source", type=input.source, defval=close)
PLACEHOLDER = input(title="PLACEHOLDER", type=input.integer, minval = 1, maxval = 50, defval = 9)
signal_length = input(title="Signal Smoothing", type=input.integer, minval = 1, maxval = 50, defval = 9)
sma_source = input(title="Oscillator MA Type", type=input.string, defval="EMA", options=["SMA", "EMA"])
sma_signal = input(title="Signal Line MA Type", type=input.string, defval="EMA", options=["SMA", "EMA"])
// Plot colors
col_macd = input(#2962FF, "MACD Line  ", input.color, group="Color Settings", inline="MACD")
col_signal = input(#FF6D00, "Signal Line  ", input.color, group="Color Settings", inline="Signal")
col_grow_above = input(#26A69A, "Above   Grow", input.color, group="Histogram", inline="Above")
col_fall_above = input(#B2DFDB, "Fall", input.color, group="Histogram", inline="Above")
col_grow_below = input(#FFCDD2, "Below Grow", input.color, group="Histogram", inline="Below")
col_fall_below = input(#FF5252, "Fall", input.color, group="Histogram", inline="Below")


DBBline     = input(false,   "══════════ Dont Buy Below══════════", type=input.bool)
smasell     = input(true,   "Sell On SMA Cross", type=input.bool)
DBBlineonoff= input(false,   "Sell On SMA Cross", type=input.bool)
lenDBA = input(180, minval=1, title="Length")
srcDBA = input(close, title="Source")

lenTREND = input(12, minval=1, title="Trend Length")
srcTREND = input(close, title="Source")
smmaTREND = 0.0
smmaTREND := na(smmaTREND[1]) ? sma(srcTREND, lenTREND) : (smmaTREND[1] * (lenTREND - 1) + srcTREND) / lenTREND
plot(smmaTREND, color=color.blue)
smmaDBA = 0.0


smmaDBA := na(smmaDBA[1]) ? sma(srcDBA, lenDBA) : (smmaDBA[1] * (lenDBA - 1) + srcDBA) / lenDBA
plot(smmaDBA, color=color.red)


//@version=4

len = input(7, minval=1, title="Length")
macdTP = input(0, "MACD TP", step = 0.01)
smma = 0.0
smma := na(smma[1]) ? sma(src, len) : (smma[1] * (len - 1) + src) / len
plot(smma, color=#673AB7)




///TP SL TSL
a_null1000     = input(false,   "══════════ Backup ORDERS ══════════", type=input.bool)
TakeProfitPercent = input(100, title="Take Profit Percent Long %", minval=0.01, step=0.01)
StopLossPercent = input(100, title="Stop Loss Percent Long %", minval=0.01, step=0.01)
longTrailPerc = input(title="Trail Long Loss (%)", type=input.float, minval=0.0, step=0.01, defval=100) * 0.01
///* 0.01
TSL = 1000
vwapsmart     = input(false,   "══════════ smart Vwap ══════════", type=input.bool)
lengthVWAP = input(20)
calc_zvwap(pds) =>
    mean = sum(volume * close, pds) / sum(volume, pds)
    vwapsd = sqrt(sma(pow(close - mean, 2), pds))
    (close - mean) / vwapsd


upperTop = input(2.5, step=0.1)
upperBottom = input(2.0, step=0.1)
lowerTop = input(-2.5, step=0.1)
lowerBottom = input(-2.0, step=0.1)
VOLtools = input(true,   "══════════ VOL TOOLS══════════ ", type=input.bool)
VOLNUM = input(-180000, step= 100, title = "NEG VOl Sell")
VOLCROSSONOFF = input(false, title= "VOL CROSS ON / OFF")
smRSIOF     = input(false,   "══════════ SMART RSI TOOLS══════════ ", type=input.bool)
len3 = input(1, minval=1, title=" Short Candle MAN Length")
src3 = input(close, title="Source")
smmarsi = 0.0
smmarsi := na(smmarsi[1]) ? sma(src3, len3) : (smmarsi[1] * (len3 - 1) + src3) / len3

upperTopRSI = (2.5)
upperBottomRSI = input(2.7, "RSI BACKUP SELL", step = .1)
lowerTopRSI = (-2.5)
lowerBottomRSI = (-2.0)
lengthRSI = input(20, "RSI length")
timedsell     = input(true,   "══════════ Timed sell══════════ ", type=input.bool)

sell_time = "374" 

/////Time Frames
////1m = 388
////5m = 76 









EMA_sell_on_off     = input(false,   "══════════ EMA sell══════════ ", type=input.bool)
lenEMA = input(9, minval=1, title="Length")
srcEMA = input(close, title="Source")

outEMA = ema(srcEMA, lenEMA)
plot(outEMA, title="EMA", color=color.green)

emasell = crossunder(close, outEMA)
plotshape(emasell ? emasell: na, title="Sell Signal", text="Sell EMA", textcolor=color.white, style=shape.labeldown, size=size.normal, location=location.abovebar, color=color.red, transp=0)
///BackTesting 
b_null18     = input(false,   "══════════ Backtesting Tools ══════════", type=input.bool)

strat_dir_input = input(title="Strategy Direction", defval="all", options=["long", "short", "all"])

strat_dir_value = strat_dir_input == "long" ? strategy.direction.long : strat_dir_input == "short" ? strategy.direction.short : strategy.direction.all

strategy.risk.allow_entry_in(strat_dir_value)
testStartYear = input(2020, "Backtest Start Year")
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(1, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay,0,0)
//Stop date if you want to use a specific range of dates
testStopYear = input(2030, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(30, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay,0,0)
testPeriod() =>
    time >= testPeriodStart and time <= testPeriodStop ? true : false
///////////////////////////////////////////////////////////////////////////////
 

// Calculating
fast_ma = sma_source == "SMA" ? sma(src, fast_length) : ema(src, fast_length)
slow_ma = sma_source == "SMA" ? sma(src, slow_length) : ema(src, slow_length)
macd = fast_ma - slow_ma
signal = sma_signal == "SMA" ? sma(macd, signal_length) : ema(macd, signal_length)
hist = macd - signal


//Strat Logic
longCondition1 = crossover(macd,signal[1]) and close
SellCondition1 = crossunder(macd,signal[1]) and (signal>0) and close and crossover(signal,macd)
SellCondition2 = crossover(signal,macdTP) and close


///Plots


//Alerts


/////Backtesting math
perc_tick = close / 100 / syminfo.mintick
ProfitTarget = (close * (TakeProfitPercent / 100)) / syminfo.mintick
LossTarget = (close * (StopLossPercent / 100)) / syminfo.mintick

is_newbar(res) =>
    t = time(res)
    not na(t) and (na(t[1]) or t > t[1])


//BUY STUFF
 ///series=showRS and lowRS ? lowRS : na, color=lowRS != lowRS[1] ? na : color.green, linewidth=4, transp=10, offset=0
plotshape(longCondition1 ? longCondition1: na, title="Buy Signal", text="Buy", textcolor=color.white, style=shape.labelup, size=size.normal, location=location.belowbar, color=color.green, transp=0)

//SELL STUFF Atheana

plotshape(SellCondition1 ? SellCondition1: na, title="Sell Signal", text="Sell", textcolor=color.white, style=shape.labeldown, size=size.normal, location=location.abovebar, color=color.red, transp=0)
plotshape(SellCondition2 ? SellCondition2: na, title="Sell Signal", text="Sell MACD TP", textcolor=color.white, style=shape.labeldown, size=size.normal, location=location.abovebar, color=color.red, transp=0)
/////////////////
///dont buy below
nv = sign(change(close)) * volume
VOLCROSS = crossunder(nv, VOLNUM)
dbb = smmaDBA < close
SMA_cross_sell = crossover(close, smmaDBA) and DBBlineonoff
smart_vwap_close = crossover(calc_zvwap(lengthVWAP),upperBottom) and vwapsmart
//////////////////

calc_zvwapRSI(pds) =>
    mean = sum(volume * smmarsi, pds) / sum(volume, pds)
    vwapsd = sqrt(sma(pow(smmarsi - mean, 2), pds))
    (smmarsi - mean) / vwapsd

SMRSICross = crossunder(calc_zvwapRSI(lengthRSI), upperBottomRSI)

betasma = open>smmaDBA
////macd_cross = crossover(fast_ma, slow_ma) 
betasell = crossunder(close,smmaDBA) 
///////TSL

longStopPrice = 0.0
shortStopPrice = 0.0

longStopPrice := if strategy.position_size > 0
    stopValue = close * (1 - longTrailPerc)
    max(stopValue, longStopPrice[1])
else
    0


trailing_stop = cross(close, longStopPrice)
plot(series=strategy.position_size > 0 ? longStopPrice : na, color=color.fuchsia, style=plot.style_linebr, linewidth=2, title="Long Trail Stop")
plotshape(trailing_stop ? trailing_stop: na, title="Sell Signal", text="Sell Take Profit", textcolor=color.white, style=shape.labeldown, size=size.normal, location=location.abovebar, color=color.red, transp=0)




///////


TREND = open > smmaTREND

////Stop trading 
stop_buying_time = true

inSession = not na (time(timeframe.period, "1549-1600"))
bgcolor(stop_buying_time and inSession ? color.silver : na)

stop_trading_time = not inSession and stop_buying_time



/////
//Main Entry and Close Cond
strategy.entry("long", strategy.long, when = longCondition1 and stop_trading_time and dbb and TREND and testPeriod(), comment="Type'HF Side'BUY Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.close("long", when = SellCondition1 and close and testPeriod(), comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.close("long", when = VOLCROSS and VOLCROSSONOFF and testPeriod(), comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.close("long", when = SellCondition2 and close and testPeriod(), comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.close("long", when = betasell and testPeriod() and smasell, comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.close("long", when = timedsell and is_newbar(sell_time) ? 1 : 0 and testPeriod(), comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.close("long", when = SMRSICross and smRSIOF and testPeriod(), comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.exit("long", "long", trail_offset = TSL *perc_tick, trail_points = TSL, profit = ProfitTarget, loss = LossTarget, comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.close("long", when = smart_vwap_close and vwapsmart and testPeriod(), comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.close("long", when = emasell and EMA_sell_on_off and testPeriod(), comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")

strategy.close("long", when = trailing_stop and testPeriod(), comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.exit("long", stop=longStopPrice, comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
strategy.exit("long", when = strategy.position_size > 0 ,stop=longStopPrice, comment="Type'HF Side'SELL Ticker'TQQQ Price'2000 Sizing'20 Filter'LARGE APIKEY'123456")
plotshape((strategy.position_size > 0) and (longStopPrice > close) and dbb, title="short Signal", text="TSL Sell ", textcolor=color.white, style=shape.labeldown, size=size.normal, location=location.abovebar, color=color.red, transp=0)