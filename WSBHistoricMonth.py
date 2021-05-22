#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### This program pretty much just loops over WSBHistoricDate. The only real difference
#### is that we hold stocks that had negative returns after holding them for 'Hold' many days another
#### 'Hold' many days. Experiments with historical Data showed that this strategy yields much better returns

import datetime as dt
import string
import json
import requests
import re
import yfinance as yf
import pandas as pd

datum = input("Please enter month and year here (MM.YYYY): ") 
hold = input("Please enter the holding duration: ")
datum2 = datum.split('.')
print('\n \n')


mret = list()

for i in range(1,31):
    try:
        startdatum = dt.datetime(int(datum2[1]),int(datum2[0]),i) 
        startdatum2 = startdatum.date()    
        enddatum = startdatum + dt.timedelta(1)
        enddatum2 = startdatum + dt.timedelta(int(hold))  
        enddatum3 = startdatum + dt.timedelta(2*int(hold))
        enddatum2 = enddatum2.date() 
        #### = one day after startdatum                   
        startdatum = startdatum.timestamp()           #### .timestamp() is needed to transform the dates into somethin useable
        enddatum = enddatum.timestamp()
    except:
        continue

    
    url1 = 'https://api.pushshift.io/reddit/search/submission/?title=What+Are+Your+Moves+Tomorrow&after='+str(int(startdatum))+'&before='+str(int(enddatum))+'&subreddit=wallstreetbets'
    r1 = requests.get(url1).text
    data1 = json.loads(r1)

    max = None

    for di in data1['data']:    
        if max == None or int(di['num_comments'])>int(max['num_comments']):
            max = di
        
    try:
        subid = max['id']    
    except:
        continue
    
    print('THIS IS THE DATA FOR ', startdatum2, '\n ')

    CommonStock = open("Tickers.txt")     
    Commondict = dict()

    for line in CommonStock:    
        line = line.rstrip()
        Commondict[line] = 0
    
    url = 'https://api.pushshift.io/reddit/comment/search/?link_id='+subid+'&limit=25000'
    r = requests.get(url).text
    data = json.loads(r)        
    
    print('Number of comments: ',len(data['data']),'\n')
    
    if len(data['data']) < 500:
        continue
        
    for i in range(len(data['data'])-1):
        body = data['data'][i]['body']
        words = re.findall('[A-Z][A-Z]+', body)
        for word in list(dict.fromkeys(words)):
            if word in Commondict and word != 'DD':    
                Commondict[word] = Commondict[word] + 1
            
    tmp = list()
        
    for key, value in Commondict.items():
        tmp.append((value,key))

    tmp.sort(reverse=True)
    print('Top 20: ',tmp[:20], "\n")    

    Top = list()

    for t in tmp[:20]:
        Top.append(t[1])
    
    dret = list()
    
    largest = None
    
    for tip in Top:
        try:
            ticker = yf.Ticker(tip)
            hist = ticker.history(start=startdatum2, end=enddatum2) 
            histpd = pd.DataFrame(hist)
            beginning = histpd.iat[0,3]
            end = histpd.iat[-1,3]
            
            if float(end)-float(beginning) >= 0:
                ret = 100/float(beginning)*(float(end)-float(beginning))
            else:
                hist2 = ticker.history(start=startdatum2, end=enddatum3)
                histpd2 = pd.DataFrame(hist2)
                end2 = histpd2.iat[-1,3]
                ret = 100/float(beginning)*(float(end2)-float(beginning))
                
            if largest == None or (ret, tip) > largest:
                largest = (ret, tip) 
                
            dret.append(ret)
            print(tip, round(ret,2))
            
        except:
            continue
    avg = round(sum(dret)/len(dret),2)        
    print('\nAverge return for ', startdatum2, 'is ', avg, '\n')
    print('Best beforming stock was: ', (round(largest[0],2), largest[1]), '\n \n \n')
    mret.append(avg) 

if len(mret) != 0:
    print('Return averaged over all days of the given month if you held the top 8 picks of each day for the specified holding duration \n', round(sum(mret)/len(mret),2) )


# In[ ]:




