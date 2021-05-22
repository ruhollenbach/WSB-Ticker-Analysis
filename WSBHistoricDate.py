#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### For a given date, this program scans all comments of the Daily Discussion thread called 
#### "What Are Your Moves Tomorrow" of r/wallstreetbets of that date (if existing), counts how often each Ticker 
#### Symbol in CommonStock.txt is mentioned and then calculates the return for each of the TOP10 stocks if we held it 
#### for 'Hold' many days

import datetime as dt
import string
import json
import requests
import re
import yfinance as yf
import pandas as pd

datum = input("Please enter date here (DD/MM/YYYY): ")  #### dates are given in european style...
datum = datum.split('.')
Hold = input("Please enter holding duration: ")

##### Just date conversions and stuff #####

try:
    startdatum = dt.datetime(int(datum[2]),int(datum[1]),int(datum[0]))   #### ...and then transformed
    startdatum2 = startdatum.date()    
    enddatum = startdatum + dt.timedelta(1)  #### used to get the correct submission.id from the pushshift API
    enddatum2 = startdatum + dt.timedelta(int(Hold))  
    enddatum2 = enddatum2.date()                  
    startdatum = startdatum.timestamp()           #### .timestamp() is needed to transform the dates into somethin useable
    enddatum = enddatum.timestamp()
except:
    print('Please enter a valid date!')
    
###########################################
    
##### Next we get the submission ID of the WAYMT-Thread for the given date ######    

url1 = 'https://api.pushshift.io/reddit/search/submission/?title=What+Are+Your+Moves+Tomorrow&after='+str(int(startdatum))+'&before='+str(int(enddatum))+'&subreddit=wallstreetbets'
print('\n',url1,'\n')
r1 = requests.get(url1).text
data1 = json.loads(r1)

max = None

for di in data1['data']:    #### this has to be done because sometimes data1 contains a few 'submissions' that we are not interested in 
    if max == None or int(di['num_comments'])>int(max['num_comments']):
        max = di
        
try:
    subid = max['id']    #### this is the submission id that we need to get the comments
except:
    print('There is no "What Are Your Moves"-Thread for this date!')   

##################################################################################


CommonStock = open("Tickers.txt")      #### opens the Tickers.txt file containing all the more-or-less major Ticker Symbols
Commondict = dict()

for line in CommonStock:     #### creates a dictionary for counting the number of times a ticker is mentioned
    line = line.rstrip()
    Commondict[line] = 0

##### Now we fetch up to 25000 comments from the WAYMT-Thread #####

url = 'https://api.pushshift.io/reddit/comment/search/?link_id='+subid+'&limit=25000'
print(url,'\n')
r = requests.get(url).text
data = json.loads(r)         

###################################################################

print('Number of comments: ',len(data['data']),'\n')

#### Next we count the mentions of each ticker found in Tickers.txt ####

bs = ['IT','FOR', 'AM', 'PM','DD','BY','ON','ALL','FUD','TA','DTE','ARE','GO'] #### a list of possible Tickers that are usually used in a different context
for i in range(len(data['data'])-1):
    body = data['data'][i]['body']
    words = re.findall('[A-Z][A-Z]+', body)
    for word in words:
        if word in Commondict and word not in bs:    
            Commondict[word] = Commondict[word] + 1
            
########################################################################
            
tmp = list()

#### We sort the Ticker-Symbols by mentions and print the TOP10 mentioned Tickers ####

for key, value in Commondict.items():
    tmp.append((value,key))

tmp.sort(reverse=True)
print('Top 10: ',tmp[:10], "\n \n")     #### top 8 Tickers with most mentions

######################################################################################
Top = list()

for t in tmp[:10]:
    Top.append(t[1])

##### For each Ticker in the TOP10 we get historic stock data from Yahoofinance and calculate the
##### possible return if we bought the stock at 'startdatum' and sold 180 days later. (Note that 'end' below 
##### is either the stockprice after 180 days or the last stock price available on Yahoo finance if 'enddatum2' is in the future)
    
for tip in Top:
    try:
        ticker = yf.Ticker(tip)
        hist = ticker.history(start=startdatum2, end=enddatum2) 
        histpd = pd.DataFrame(hist)
        beginning = histpd.iat[0,3]
        end = histpd.iat[-1,3]
        ret = 100/float(beginning)*(float(end)-float(beginning))
        print(tip, '     ', round(beginning,3), '    ', round(end,3), '     Return: ', round(ret,2),'%', '\n', hist['Close'], '\n \n')
    except:
        print('\n \n')
        continue

#################################################################################################


# # 

# In[ ]:




