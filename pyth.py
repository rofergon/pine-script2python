import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import os
from selenium import webdriver


def get_file_path(folder_path, file_name):
    path = os.getcwd() + folder_path
    file_path = path + file_name
    return file_path


def get_page_urls(url):
    webdriver.get(url)
    pages = webdriver.find_elements_by_class_name('screener-pages')
    last_page = int(pages[-1].text)
    url_list = [url]
    for i in range(1, last_page):
        text = '&r=' + str(i * 20 + 1)
        url_list.append(url+text)
    return url_list


def get_ticker_symbols(url):
    webdriver.get(url)
    symbols = webdriver.find_elements_by_class_name('screener-link-primary')
    ticker_list = []
    for sym in symbols:
        ticker_list.append(sym.text)
    return ticker_list

def get_sma(ser, days):
    sma = ser.rolling(window=days).mean()
    return sma


def get_ema(ser, days):
    sma = ser.rolling(window=days, min_periods=days).mean()[:days]
    rest = ser[days:]
    ema = pd.concat([sma, rest]).ewm(span=days, adjust=False).mean()
    return ema


def check_triangle(stock):
    yf.pdr_override()
    end_date = dt.datetime.today()
    start_date = end_date - dt.timedelta(days=365*2)

    df = pdr.get_data_yahoo(stock, start_date, end_date)

    df['sma25'] = get_sma(df['Adj Close'], 25)
    df['sma50'] = get_sma(df['Adj Close'], 50)
    df['sma200'] = get_sma(df['Adj Close'], 200)
    df['ema5'] = get_ema(df['Adj Close'], 5)
    df['ema33'] = get_ema(df['Adj Close'], 33)

    df['test1'] = np.where((df['ema5'] > df['sma50']), 1, -1)
    df['test2'] = df['test1'].shift(periods=1)
    df['test3'] = df['test1'] - df['test2']
    df['test4'] = np.where((df['test3'] == 2) & (
        df['ema33'] > df['sma50']), -1, 0)

    if df['test4'][-1] == -1:
        return stock
    else:
        return 0


stocks = ['BTC-USD', 'LTC-USD', 'A', 'AA', 'AAAU', 'AACG', 'AADR', 'AAIC']

picks = []

for stock in stocks:
    pick = check_triangle(stock)
    if pick != 0:
        picks.append(pick)

print(picks)
