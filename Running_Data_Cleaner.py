import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
df = pd.read_csv("Activities.csv", usecols = ['Date', 'Distance', 'Avg Pace','Avg Stride Length', 'Avg Run Cadence' ], parse_dates = ['Date'])

e = 0
for i in df.iterrows():
    df.at[e,'Date'] = str(df.at[e,'Date'])[:10]
    df.at[e,'Avg Pace'] = df.at[e,'Avg Pace'].split(':')
    df.at[e,'Avg Pace'] = int(df.at[e,'Avg Pace'][0]) * 60 + int(df.at[e,'Avg Pace'][1])
    e += 1
df.rename(columns={'Avg Pace':'Pace'}, inplace=True)
df.rename(columns={'Avg Stride Length':'Stride'}, inplace=True)
df.rename(columns={'Avg Run Cadence':'Cadence'}, inplace=True)

df.Pace = df.Pace.astype('int') 
gf = df.groupby([pd.Grouper(key='Date', freq='Y')])['Distance'].sum().reset_index()
pf = df.groupby([pd.Grouper(key='Date', freq='Y')])['Pace'].mean().reset_index().sort_values('Date')
sf = df.groupby([pd.Grouper(key='Date', freq='Y')])['Stride'].mean().reset_index().sort_values('Date')
cf = df.groupby([pd.Grouper(key='Date', freq='Y')])['Cadence'].mean().reset_index().sort_values('Date')
gf = pd.merge(gf, pf, on=['Date'])
gf = pd.merge(gf, sf, on=['Date'])
gf = pd.merge(gf, cf, on=['Date'])


print(gf)
yf = gf
tke = 537
fke = 951
tkn = 515
fkn = 890
tkd = tke - tkn
fkd = fke - fkn
fkpd = 1 - (fkn/fke)
yf.set_index('Date', inplace = True)
yrmpd = 1 - (float(yf['2017']['Distance'])/float(yf['2018']['Distance']))
yrppd = 1 - (float(yf['2018']['Pace']) / float(yf['2017']['Pace']))
#sec = input("h")
sec = input("By how many seconds would you like to improve your 5k time? ")
print("Based on your past Garmin data, a volume of", (int(sec) * (yrmpd / fkd)) * float(yf['2018']['Distance']) + float(yf['2018']['Distance']), "miles over")
print("the next year coupled with an overall average pace of ", float(yf['2018']['Pace'])-((int(sec) * (yrppd / fkd) * float(yf['2018']['Pace']))), "may get you there.")
##print(yf)
##plt.rcParams['figure.figsize'] = (10, 5)
##ax = plt.gca()
##gf['Date'] = gf['Date'].astype(str)
##gf['Date'] = gf['Date'].str[:10]
##gf['Distance'] = gf['Distance'].astype(int)
##gf.plot.bar(x= 'Date', y=['Distance'], ax = ax)
##plt.show()

