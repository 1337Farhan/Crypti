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
    import coinbasepro
    import csv
    import sklearn
    import datetime
    
except ImportError:
    print("Trying to Install required modules\n")
    os.system('pip install -r requirements.txt')

import plotly.express as px
import pandas as pd
import numpy as np
import CryptiCLI
import coinbasepro as cbpro
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
data_1 = cbClient.get_product_historic_rates(f'{Token}'+'-USD', granularity=gran, start=api_start, stop=datetime.now())
data_2 = cbClient.get_product_historic_rates(f'{Token}'+'-USD', granularity=gran, start=api_start - timedelta(days=gran*300/86400), stop=api_start)
data = data_1 + data_2 # data -> [ time, low, high, open, close, volume ]

# convert UNIX time to str 24h time
for candle in data:
    candle['time'] = candle['time'].strftime("%Y-%m-%d %H:%M:%S") # convert to readable time

# key names for csv format
keys = data[0].keys()
print(keys)
# covert array of arrays to csv
with open('CryptiFood.csv', mode='w', newline='') as outputFile:
    writer = csv.DictWriter(outputFile, keys)
    writer.writeheader()
    writer.writerows(data)

dataFile = pd.DataFrame(pd.read_csv('CryptiFood.csv')) # read csv
dataFile = dataFile.sort_values('time', ascending=True) # asc sort 

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
fig_rawData = px.line(dataFile, x = 'time', y = 'close', title=f'{Token}')
fig_rawData.show()

# predicted data
fig_PredData = px.line(x = PredictionTimestamps, y = linReg_projection, title = f'{Token} price prediction')
fig_PredData.show()

print('Confidence [Accuracy]: ' + str(linReg_confidence))

if linReg_confidence < 0.65:
    print('Confidenece level is less than 65%, consider tweaking the settings') 