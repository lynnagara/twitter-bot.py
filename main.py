import connect_to_twitter as twitter
import process_tweet
import create_tweet

default_params = {
  'screen_name': 'realDonaldTrump',
  'count': 200,
  'include_rts': False,
  'exclude_replies': True
}

def process_tweets(tweets):
  for tweet in tweets:
    print(tweet['text'])
    process_tweet.save_starting_word(tweet)
    process_tweet.build_dictionary(tweet)
    process_tweet.save_tweet_endings(tweet)

def fetch_all_tweets():
  max_id = None

  while True:
    if max_id is None:
      timeline = twitter.get_timeline(default_params)
    else:
      params = {**default_params, **{'max_id': max_id}}
      timeline = twitter.get_timeline(params)[1:]
    process_tweets(timeline)
    if (len(timeline) > 0):
      max_id = timeline[-1]['id']
    else:
      break

# Fetch all the tweets
fetch_all_tweets()

# Generate a tweet
create_tweet.make_tweet()
