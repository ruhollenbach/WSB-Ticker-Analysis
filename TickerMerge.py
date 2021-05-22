#!/usr/bin/env python
# coding: utf-8

# In[7]:


##### This little routine just merges the two lists NasdaqListed and OtherExchanges 
##### of Ticker symbols downloaded from ftp.nasdaqtrader.com and extracts the relevant information

import re
import urllib.request

Nasdaq = urllib.request.urlopen('http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt').read() ### this file is nicely formatted and can be read without any problems
Others = urllib.request.urlopen("http://ftp.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt")   ### this file on the other hand is a mess and is therefore read line by line
CommonStock = open("CommonStock.txt",'w') ### the merge is written into this file
Tickers = open("Tickers.txt","w")

common1 = re.findall("([A-Z]+\|[A-Z].+)-.+Common Stock",Nasdaq.decode())
common11 = re.findall("([A-Z]+)\|[A-Z].+-.+Common Stock",Nasdaq.decode())
common22 = list()
common2 = list()

for line in Others:
    x = re.findall("^([A-Z]+\|[A-Z].+)-* .+Common Stock",line.decode())
    y = re.findall("^([A-Z]+)\|[A-Z].+-* .+Common Stock",line.decode())
    if len(x)>0:
        common2.append(x[0])
        common22.append(y[0])
        

common3 = list()
common33 = list()

for line in common2:
    common3.append(re.sub('-* Class','',line)) ### the strings in common2 contain descriptions of the common stock
                                               ###like Class A Common Stock and we don't need that information in 
                                               ### in our list
    
for line in common22:
    common33.append(re.sub('-* Class','',line))
                                                  
for stock in common1:
    CommonStock.write(stock+'\n')

for stock in common3:
    CommonStock.write(stock+'\n')

for stock in common11:
    Tickers.write(stock+'\n')

for stock in common33:
    Tickers.write(stock+'\n')
    
CommonStock.close()
Tickers.close()


# In[ ]:




