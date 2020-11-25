import networkx as nx
import pickle
import tweepy
import json
import datetime
from itertools import combinations
import credentials

WORDS = ['#brexit','#antibrexit','#stopbrexit']

consumer_key , consumer_secret , access_key , access_secret = credentials.return_keys()


class StreamListener(tweepy.StreamListener):
    #This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        file = open('test.txt','a')
        try:
            taglist = []
            datajson = json.loads(data)
            hashtags = datajson['entities']['hashtags']
            for h in hashtags:
                taglist.append(h['text'])
            combo = list(combinations(taglist, 2))
            for c in combo:
                file.write(str(c[0])+','+str(c[1])+'\n')
        except Exception as e:
           print(e)
        file.close()


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True,wait_on_rate_limit_notify=True,compression=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
#print("Tracking: " + str('United Kingdom'))
streamer.filter(track=WORDS)



