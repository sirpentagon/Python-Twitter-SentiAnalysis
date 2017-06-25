"""
Created on Wed Jun 07 01:08:04 2017

@author: Arijit
"""
import sys
import tweepy
import readIMDB as imdb
from textblob import TextBlob
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

class TweetListener(StreamListener):
    def __init__(self, api=None,list_=None,dict_=None,imdbdata_=None):
        self.api = api
        self.keys_= list_
        self.dict = dict_
        self.imdbdata = imdbdata_
        
    def on_status(self, status):   
        str_ = status.text.lower()        
        for key in self.dict.keys():
            if key.lower() in str_.lower():
                if self.dict[key] <= 0:
                    return True
                else:
                    self.dict[key] -=1
                    self.__sentianalysis(key,status)                                      
                    
        if all(value == 0 for value in self.dict.values()):
            return False
                    
    def on_error(self, status):        
        print status
        if status == 420:
            print "Too soon reconnected . Will terminate the program"
            return False
        sys.exit()        
        
    def __sentianalysis(self,key,status):
        blob = TextBlob(status.text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity
        for i in range(0,len(self.imdbdata)):
            if self.imdbdata[i]['name'] == key:                                        
                print "Name of the celebrity : %s" % key
                print "Celebrity Image : %s" %self.imdbdata[i]['image']
                print "Profession : %s" % self.imdbdata[i]['profession']
                print "Best Work : %s" % self.imdbdata[i]['bestwork']    
                if polarity < 0:
                    print "Overall Sentiment - Negative"
                elif polarity == 0:
                    print "Overall Sentiment - Neutral"
                elif polarity > 0:
                    print "Overall Sentiment - Positive"
                if subjectivity < 0.5:
                    print "Statement tends very objective"
                elif subjectivity >= 0.5:
                    print "Statement tends very subjective"
                print "Tweet Text : %s" % status.text
                print "\n\n"
        
        
###############################################################################

def connect():
    consumer_key = #ENTER YOUR CONSUMER KEYS
    consumer_secret = #ENTER YOUR CONSUMER SECRET
    access_token = #ENTER YOUR ACCESS TOKEN
    access_secret = #ENTER YOUR ACCESS SECRET

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5,
                     retry_errors=5)
    return api

def create_dict(list_):
    no_of_tweets = 2
    dict_ =  {k:no_of_tweets for k in list_ }
    return dict_

def search_tweets(imdb_data):
    api = connect()
    search_words_list = []
    for i in range(0,len(imdb_data)):
        search_words_list.append(imdb_data[i]['name'])
    twitterStream = Stream(api.auth, TweetListener(api=api,
                                                   list_=search_words_list, 
                                                   dict_=create_dict(search_words_list),
                                                   imdbdata_=imdb_data))
    twitterStream.filter(track=search_words_list, languages=["en"], async=True)

def main():
    imdb_obj = imdb.IMDB()
    imdb_data = imdb_obj.getdata()
    search_tweets(imdb_data)

main()