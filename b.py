import numpy as np
import pandas as pd
import pandas_datareader as pdr
from pandas_datareader import data as wb
from pandas_datareader._utils import RemoteDataError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import csv

tickerList = pd.read_csv("docs/Viop.csv")
tickers=tickerList["Ticker"]
# start_date=(date.today()-timedelta(days=360))
start_date=(date.today()-relativedelta(years=1))
data_source='yahoo'
for i in tickers:
    ticker = i
    ticker_data=wb.DataReader(ticker,data_source=data_source,start=start_date)
    df=pd.DataFrame(ticker_data)
    ticker_date=ticker_data.index
    last_10_days_lastDayExcluded=ticker_date[-10:-1]
    c=df['Close']
    h=df['High']
    l=df['Low']
    last_price=c[-1]
    maxInDate=max(h[ticker_date])
    minInDate=min(l[ticker_date])
    max10=max(h[last_10_days_lastDayExcluded])
    min10=min(l[last_10_days_lastDayExcluded])
    potentialReward=max10-last_price
    risk=last_price-min10
    recommendationList=['Yeni Dip Yapıyor Pozisyona Girme','Yeni Zirve Arayışı','AL','Pozisyona Girme']
    new_low=str(recommendationList[0])
    new_high=str(recommendationList[1])
    buy=str(recommendationList[2])
    dontBuy=str(recommendationList[3])
    def tradeable():
        if (last_price<min10):
            str_ticker=str("{}".format(ticker))
            recommendation=new_low
            str_lastPrice=str("{:.2f} ".format(c[-1]))
            str_earn_potential=''
            str_loss_potential=''
            str_target_SalePrice=''
            str_stopLoss=''
            if(minInDate<last_price):
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_stopLoss=str("{:.2f}".format(minInDate))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
            return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
        elif (last_price>max10):
            str_ticker=str("{}".format(ticker))
            recommendation=new_high
            str_lastPrice=str("{:.2f} ".format(c[-1]))
            str_earn_potential=''
            str_loss_potential=str("{:.2f}".format(last_price-max10))
            str_target_SalePrice=''
            str_stopLoss=str("{:.2f}".format(max10))
            if(maxInDate>last_price):
                if((maxInDate-last_price)*2>(last_price-max10)):
                    recommendation=buy
                else:
                    recommendation=dontBuy
                str_earn_potential=str("{:.2f}".format(maxInDate-last_price))
                str_target_SalePrice=str("{:.2f}".format(maxInDate))
            return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
        else:
            if (potentialReward>risk*2):
                str_ticker=str("{}".format(ticker))
                recommendation=buy
                str_stopLoss=str("{:.2f}".format(min10))
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=str("{:.2f}".format(potentialReward))
                str_loss_potential=str("{:.2f}".format(risk))
                str_target_SalePrice=str("{:.2f}".format(max10))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss   

            else:
                str_ticker=str("{}".format(ticker))
                recommendation=dontBuy
                str_stopLoss=str("{:.2f}".format(min10))
                str_lastPrice=str("{:.2f} ".format(c[-1]))
                str_earn_potential=str("{:.2f}".format(potentialReward))
                str_loss_potential=str("{:.2f}".format(risk))
                str_target_SalePrice=str("{:.2f}".format(max10))
                str_stopLoss=str("{:.2f}".format(min10))
                return str_ticker,recommendation,str_lastPrice,str_earn_potential,str_loss_potential,str_target_SalePrice,str_stopLoss
    print(tradeable())
    
