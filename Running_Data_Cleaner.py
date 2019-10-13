import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
df = pd.read_csv("Activities.csv", usecols = ['Date', 'Distance', 'Avg Pace'], parse_dates = ['Date'])

#Convert avg pace from minutes per mile to seconds per mile for simplicity
#Strip time stamp from date column
e = 0
for i in df.iterrows():
    df.at[e,'Date'] = str(df.at[e,'Date'])[:10]
    df.at[e,'Avg Pace'] = df.at[e,'Avg Pace'].split(':')
    df.at[e,'Avg Pace'] = int(df.at[e,'Avg Pace'][0]) * 60 + int(df.at[e,'Avg Pace'][1])
    e += 1

df.rename(columns={'Avg Pace':'Pace'}, inplace=True)    
df.Pace = df.Pace.astype('int') 

#Combine distance and pace from any days that are non-distinct (i.e. double runs)
mf = df.groupby(['Date'])['Distance'].apply(lambda x: sum(x)).reset_index()
cf = df.groupby(['Date'])['Pace'].apply(lambda x: sum(x)).reset_index()
df = pd.merge(mf, cf, on=['Date'])
e = 0

#Any day that has a pace over 600 is a double day.
for i in df.iterrows():
    if df.at[e,'Pace'] > 600:
        df.at[e,'Pace'] = df.at[e,'Pace']/2
    e += 1

#Group runs together by week and compute average distance and pace for the week. Put into
#new dataframes for later
gf = df.groupby([pd.Grouper(key='Date', freq='W-SUN')])['Distance'].mean().reset_index().sort_values('Date')
pf = df.groupby([pd.Grouper(key='Date', freq='W-SUN')])['Pace'].mean().reset_index().sort_values('Date')

#Insert missing days within the dataframe with Nan for distance val
df.set_index('Date', inplace = True)
df = df.resample("D").mean()
#df = df['2019']

#Drop indexes and fill any Nan's with 0's for simplicity
gf = gf.reset_index()
df = df.reset_index()
pf = pf.reset_index()
##print(df)
df = df.fillna(0)

#For every day that has been inserted, insert the average distance and pace of runs
#for the specific week that day resides in. 
e = 0
for i in df.iterrows():
    if df.at[e,'Distance'] == 0: 
        rep = df.at[e,'Date']     #Day that has no data
        r = 0
        for j in gf.iterrows():  
            if rep < gf.at[r,'Date']:   #gf's dates are weekly.
                df.at[e,'Distance'] = gf.at[r,'Distance']
                df.at[e,'Pace'] = pf.at[r,'Pace']
                break
            r += 1
    e += 1

#Find the averages of the data by year and create a new data frame for calculations 
gf = df.groupby([pd.Grouper(key='Date', freq='Y')])['Distance'].sum().reset_index().sort_values('Date')
lf = df.groupby([pd.Grouper(key='Date', freq='Y')])['Pace'].mean().reset_index().sort_values('Date')
df = pd.merge(gf, lf, on=['Date'])
##print(gf.head())
##print(gf.groupby([pd.Grouper(key='Date', freq='M')])['Distance'].mean())
##plt.rcParams['figure.figsize'] = (10, 5)
##ax = plt.gca()
##gf['Date'] = gf['Date'].astype(str)
##gf['Date'] = gf['Date'].str[:10]
##gf.plot.line(x='Date',y=['Distance','Pace', '5k', '3k'], ax = ax)
###gf.plot(kind='line',x='name',y='num_pets', color='red', ax=ax)
##
##plt.show()

