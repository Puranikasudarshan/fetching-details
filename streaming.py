import tweepy
import json
from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost/twitterdb'
WORDS = ['RTed']
 

consumer_key = "your consumer key"
consumer_secret = "your consumer secret"
access_token = "your access token"
access_token_secret = "your access token secret"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)
query = "RTed"
language = "en"
results = api.search(q=query,lang=language)
#for tweet in results:
#  print(tweet.user.screen_name,"tweeted:",tweet.text)

class StreamListener(tweepy.StreamListener):
 def on_connect(self):
  print("you are now connected")

 def on_error(self,status_code):
  print("an error has occured: "+ repr(status_code))
  return False

 def on_data(self,data):
  try:
      client = MongoClient(MONGO_HOST)
      db = client.twitterdb
      query = "RTed"
      language = "en"
      results = api.search(q=query,lang=language)
      
      results_json = list()
      for result in results:
	results_json.append({"text": result.text, "name": result.user.name})
      db.twitter_collection.insert(results_json)
      print("successfully inserting")
  except Exception as e:
      print(e)

listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
