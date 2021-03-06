# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:20:42 2020

@author: Jenny Lu
"""

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
from matplotlib.dates import MonthLocator,MONTHLY
import datetime as dt
import pylab

daylinefilespath = 'test.xlsx'
stock_b_code = 'abc001' #股票名称
MA1 = 10
MA2 = 50
startdate = dt.date(2019, 1, 1)
enddate = dt.date(2020, 3, 26)


def readstkData(rootpath, stockcode, sday, eday):
    
#    returndata = pd.DataFrame()
#    for yearnum in range(0,int((eday - sday).days / 365.25)+1):
#        theyear = sday + dt.timedelta(days = yearnum * 365)
#        # build file name
#        filename = rootpath
#        rawdata = pd.read_excel(filename, sheetname=stock_b_code, index_col = 0, encoding = 'gbk')
#
#        returndata = pd.concat([rawdata, returndata])
    
        # build file name
    filename = rootpath
    returndata = pd.read_excel(filename, sheet_name=stock_b_code, index_col = 0, encoding = 'gbk')
    returndata = pd.DataFrame(returndata)
    
    # Wash data
    returndata = returndata.sort_index()
    returndata.index.name = 'DateTime'
#    returndata.drop('amount', axis=1, inplace = True)
    returndata.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    returndata = returndata.ix[3:]# 删除多余的行
    returndata = returndata.dropna(axis=0,how='all')
    print(returndata)
#    returndata = returndata[returndata.index < eday.strftime('%Y-%m-%d')]
    return returndata

def movingaverage(data, window_size):
#    data=float(data)
    cumsum_vec = np.cumsum(np.insert(data, 0, 0)) 
    ma_vec = (cumsum_vec[window_size:] - cumsum_vec[:-window_size]) / window_size
    print(ma_vec)
    return ma_vec


def main():
    days = readstkData(daylinefilespath, stock_b_code, startdate, enddate)

    # drop the date index from the dateframe & make a copy
#    daysreshape = days.reset_index()
    # convert the datetime64 column in the dataframe to 'float days'
#    daysreshape['DateTime']=mdates.date2num(daysreshape['DateTime'].astype(dt.date))
#    daysreshape['DateTime']=mdates.date2num(daysreshape['DateTime'])
    (m, n)=np.shape(days)
    for i in range(0, m):
        date_time = datetime.datetime.strptime(days.index.values[i].replace(" ", ""), '%Y/%m/%d')
        days.index.values[i] = mdates.date2num(date_time)
    # clean day data for candle view 
    days.drop('Volume', axis=1, inplace = True)
    days = days.reindex(columns=['DateTime','Open','High','Low','Close'])  
    
#    Av1 = movingaverage(daysreshape.Close.values, MA1)
#    Av2 = movingaverage(daysreshape.Close.values, MA2)
    SP = len(days.DateTime.values[MA2-1:])
    fig = plt.figure(facecolor='#07000d',figsize=(15,10))
    
    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, facecolor='#07000d')
#    ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
    candlestick_ohlc(ax1, days.values[-SP:], width=.6, colorup='#ff1717', colordown='#53c156')
    Label1 = str(MA1)+' SMA'
    Label2 = str(MA2)+' SMA'
    
#    ax1.plot(daysreshape.DateTime.values[-SP:],Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
#    ax1.plot(daysreshape.DateTime.values[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')
    plt.show()

if __name__ == "__main__":
    main()