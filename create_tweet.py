import random
import pickle
import utilities

def get_first_word():
  file = open('starting_words.txt', 'r')
  lines = file.readlines()
  length = len(lines)
  random_word = lines[random.randrange(length)].replace('\n', '')
  return random_word

def get_next_word(previous):
  # Fetch file with word
  filename = utilities.to_file_name(previous.split()[0])

  file = pickle.load(open('words/' + filename, 'rb'))

  if previous in file:

    next_words = file[previous]

    # Create an array with every occurance of a word
    words = []
    for word_or_words in next_words:
      words += next_words[word_or_words] * [word_or_words]

    # Pick a random word
    random_word = words[random.randrange(len(words))]
    return random_word

  else:
    return utilities.end_of_tweet_marker()


def make_tweet():
  tweet = []

  # Get the first word
  first_word = get_first_word()
  tweet.append(first_word)

  # Populate second word
  while True:
    if (len(tweet) > 1):
      previous_word_or_words = str.join(' ', tweet[-2:])
    else:
      previous_word_or_words = tweet[-1]

    next_word = get_next_word(previous_word_or_words)

    if (next_word == utilities.end_of_tweet_marker()):
      break
    else:
      tweet.append(next_word)

  print(str.join(' ', tweet))



