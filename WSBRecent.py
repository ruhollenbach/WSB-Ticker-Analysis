#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#### This program is similar to WSBHistoricDate. However, the goal is to fetch and analyse comments 
#### from the most recent threads. The Pushshift Database is updated too slowly for that which means that 
#### we have to use the original Reddit API or PRAW. The program writes the TOP20 stocks + up to 15 comments 
#### per stock in a file. We return 15 comments because we were too lazy to implement an automated sentiment check.
#### Many comments in WSB are of the form "RIP TSLA PUTS". Any simple sentiment checker would considere that 
#### a negative statement about TSLA because the words RIP and PUTS appear even though it is clearly positive. So for
#### now, one has to read some of the comments themselves to see what the sentiment is (if there is one).

import datetime as dt
import string
import praw
import json
import requests
import re



datum = input("Please enter date here (DD/MM/YYYY): ")  
datum2 = datum.split('.')


#### Just date conversions and stuff

try:
    startdatum = dt.datetime(int(datum2[2]),int(datum2[1]),int(datum2[0]))   
    enddatum = startdatum + dt.timedelta(1)                  
    startdatum = startdatum.timestamp()           
    enddatum = enddatum.timestamp()
except:
    print('Please enter a valid date!')
    
reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    redirect_uri="REDIRECT_URI",
    user_agent="USER_AGENT",
)

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
    print("Invalid!")

submission = reddit.submission(id=max['id'])

print(submission.title)

CommonStock = open("Tickers.txt")     

Commoncount = dict()
CommonComment = dict()

for line in CommonStock:     
    line = line.rstrip()
    Commoncount[line] = 0
    CommonComment[line] = list()



bs = ['IT','FOR', 'AM', 'PM','DD','BY','ON','ALL','FUD','TA','DTE','ARE','GO']

count = 0 

submission.comments.replace_more(limit=None)

for comment in submission.comments.list():
    count = count +1
    print(count)
    words = re.findall('[A-Z][A-Z]+', comment.body)
    for word in list(dict.fromkeys(words)):
        if word in Commoncount and word not in bs:    
            Commoncount[word] = Commoncount[word] + 1
            CommonComment[word].append(comment.body.strip().encode('ascii','ignore'))
            
tmp = list()
        
for key, value in Commoncount.items():
    tmp.append((value,key))

tmp.sort(reverse=True)
print("\n",count, "\n\n")
print('Top 10: ',tmp[:10], "\n") 

WSB = open("WSB_Top20_"+datum+".txt","w")

for tip in tmp[:20]:
    WSB.write('{0}:  {1}\n'.format(tip[1], tip[0]))

WSB.write("\n\n\n Selection of Comments:\n\n")
    
for tip in tmp[:20]:
    WSB.write("\n\n\n")
    WSB.write(tip[1])
    WSB.write("\n\n\n")
    for comment in CommonComment[tip[1]][:15]:
        WSB.write("- "+comment.decode()+"\n")
        
WSB.close()


# In[ ]:




