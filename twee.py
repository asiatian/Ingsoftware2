import tweepy

consumer_key="3m5QUlAmS9NEvG8DNtDjeEBQ8"
consumer_secret="p5QfzLdPPCoS3B6v6KMKB7cqqMWVsP07IbXaCZVmRKJ6Mv6HvZ"
access_token="850458844975308800-SJuKvqs5J57FUjCgH0KXDCnPKPtiVCM"
access_token_secret="PuEJ039IwTz5CfP6Oxn3a68Tdh8hcRsshlwkfJakPRO0n"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)

auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

import sys
import jsonpickle
import os
from datetime import datetime, timedelta

if len(sys.argv) == 1:
	print("ERROR")
	exit()

searchQuery= sys.argv[1]
maxTweets = 10000
tweetsPerQry = 45
folderName = str(datetime.now().date()-timedelta(1))
if not os.path.exists(folderName):
	os.makedirs(folderName)
fName = searchQuery+'.json'

sinceId = None
max_id = -1
tweetCount = 0
salir = 0
print("Descargando max {0} tweets".format(maxTweets))
with open(folderName+'/'+fName, 'w') as f:
    while (tweetCount < maxTweets) and (salir == 0):
        try:
            if (max_id <= 0):
                if(not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1), since_id=sinceId)
            if not new_tweets:
                print("No hay nuevos tweets")
                break

            for tweet in new_tweets:
            	if( datetime.now().date()-timedelta(1) > tweet.created_at.date()):
            		salir=1
            		break
            	else:
                	f.write(jsonpickle.encode(tweet._json) + '\n')
            tweetCount += len(new_tweets)
            print("Se descargaron {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print("Error! " + str(e))
            break
print("Descargados {0} tweets, guardados en {1}".format(tweetCount,fName))