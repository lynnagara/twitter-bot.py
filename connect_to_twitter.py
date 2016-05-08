import oauth2 as oauth
import urllib
import json
import configparser

# Keys
config = configparser.ConfigParser()
config.read('settings.ini')

consumer = oauth.Consumer(
  key = config['Twitter']['consumer_key'], 
  secret = config['Twitter']['consumer_secret']
)

client = oauth.Client(consumer)

# Get twitter timeline
def get_timeline(params={}):
  timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
  url = timeline_url + '?' + urllib.parse.urlencode(params)

  response = client.request(url, 'GET')
  body = response[1].decode('utf-8')
  return json.loads(body)
