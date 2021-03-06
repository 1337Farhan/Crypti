import os
import sys

if sys.version_info < (3, 0):
    print('Please upgrade your Python version to python3')
    sys.exit()

try:
    import plotly
    import plotly.express
    import pandas
    import numpy
    import cbpro
    import csv
    import sklearn
    import datetime
    
except ImportError:
    print("Trying to Install required modules\n")
    os.system('pip3 install plotly.express')
    os.system('pip3 install plotly')
    os.system('pip3 install pandas')
    os.system('pip3 install numpy')
    os.system('pip3 install cbpro')
    os.system('pip3 install csv')
    os.system('pip3 install sklearn')
    os.system('pip3 install datetime')


import plotly.express as px
import pandas as pd
import numpy as np
import CryptiCLI
import cbpro
import csv
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


CryptiCLI.Welcome()

Token = CryptiCLI.chooseToken()

gran = CryptiCLI.chooseGranularity()

candles = CryptiCLI.num_of_candles()

# tSize = CryptiCLI.testSize() # For testing purposes, default = 0.15

cbClient = cbpro.PublicClient()


# granularity 60, 300, 900, 3600, 21600, 86400
api_start = datetime.now() - timedelta(days=gran*300/86400)
data_1 = cbClient.get_product_historic_rates(f'{Token}'+'-USD', granularity=gran, start=api_start, end=datetime.now())
data_2 = cbClient.get_product_historic_rates(f'{Token}'+'-USD', granularity=gran, start=api_start - timedelta(days=gran*300/86400), end=api_start)

data = data_1 + data_2 # data -> [ time, low, high, open, close, volume ]


# convert UNIX time to str 24h time
for candle in data:
    candle[0] = datetime.fromtimestamp(candle[0]).strftime("%Y-%m-%d %H:%M:%S") # convert to readable time

# key names for csv format
keys = ['timestamp', 'low', 'high', 'open', 'close', 'vol']

# covert array of arrays to csv
with open('CryptiFood.csv', mode='w') as inputFile:
    writer = csv.writer(inputFile)
    writer.writerow(keys)
    writer.writerows(data)

dataFile = pd.DataFrame(pd.read_csv('CryptiFood.csv')) # read csv
dataFile = dataFile.sort_values('timestamp', ascending=True) # asc sort 

projection = candles # number of data points to be predicted
dataFile['Prediction'] = dataFile[['close']].shift(-projection) # shifting the close price of each day -[projection] rows

x = np.array(dataFile[['close']]) # copy the close column
x = x[:-projection] # remove the latest [projection] close prices

y = dataFile['Prediction'].values # copy the [prediction] values column
y = y[:-projection] # remove the latest [projection] predicted prices since we don't have them yet

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15) # split the datasets to test and train subsets (for testing use tSize)

linReg = LinearRegression() # choosing the LR model

linReg.fit(x_train, y_train) # find the coefficients for the LR equation

linReg_confidence = linReg.score(x_test, y_test) # calculate confidence

x_projection = np.array(dataFile[['close']])[-projection:] # prepare the data for time projection

linReg_projection = linReg.predict(x_projection) # perform the projection


PredictionTimestamps = [] # list of timestamps for predicted prices

TempTimestamp = datetime.strptime(data[0][0], "%Y-%m-%d %H:%M:%S") # temporary time

# create the timestamps for plotting predicted prices
for i in range(1, projection+1):
    TempTimestamp = TempTimestamp + timedelta(days=(gran/86400))
    PredictionTimestamps.append(TempTimestamp)

# plotting the data

# training data
fig_rawData = px.line(dataFile, x = 'timestamp', y = 'close', title=f'{Token}')
fig_rawData.show()

# predicted data
fig_PredData = px.line(x = PredictionTimestamps, y = linReg_projection, title = f'{Token} price prediction')
fig_PredData.show()

print('Confidence [Accuracy]: ' + str(linReg_confidence))

if linReg_confidence < 0.65:
    print('Confidenece level is less than 65%, consider tweaking the settings') 