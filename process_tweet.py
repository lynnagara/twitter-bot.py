import re
import os
from pathlib import Path
import pickle
import binascii

def to_file_name(text):
  return binascii.hexlify(text.encode()).decode('utf-8')

def from_file_name():
  return binascii.unhexlify(file_name).decode('utf-8')

def sanitize_tweet(tweet):
  return strip_multi_spaces(strip_urls(tweet))

def strip_forward_slash(text):
  pattern = r'/'
  return re.sub(pattern, '', text)

def strip_multi_spaces(text):
  pattern = r' +'
  return re.sub(pattern, ' ', text)

def strip_urls(text):
  pattern = r'https?://.+'
  return re.sub(pattern, '', text)  

def save_starting_word(tweet):
  filename = 'starting_words.txt'
  text = tweet['text']
  sanitized_text = sanitize_tweet(text)
  # Just save the starting word in the text file unless it starts special chars
  if (len(text) > 0 and text[0] != '@' and text[0] != '.' and text[0] != '#'):
    first_word = text.split(' ')[0]
    target = open(filename, 'a')
    target.write(first_word + '\n')

# Get each pair and triplet of words
def get_word_groups(text):
  word_groups = []

  words = text.split(' ')

  for idx, word in enumerate(words):
    # Add groups of two words
    if (idx > 0):
      word_slice = words[idx-1:idx+1]
      word_groups.append(word_slice)

    # Add groups of three words
    if (idx > 1):
      word_slice = words[idx-2:idx+1]
      word_groups.append(word_slice)

  return word_groups

def create_words_folder():
  try:
    os.makedirs('words')
  except:
    pass

def save_word_group(word_group):
  # Just try to create the folder
  create_words_folder()
  filename = to_file_name(word_group[0])
  file_exists = Path('words/' + filename).exists()

  # Update store with new words
  key = str.join(' ', word_group[:-1])
  next_word = word_group[-1]

  if (file_exists):
    data = pickle.load(open('words/' + filename, 'rb+'))

    # Is the key already there?
    if key in data:
      if next_word in data[key]:
        # increment counter
        data[key][next_word] += 1
      else:
        data[key][next_word] = 1

    else:
      data[key] = {
        next_word: 1
      }

  else:
    data = {
      key: {
        next_word: 1
      }
    }
  pickle.dump(data, open('words/' + filename, 'wb'))

def build_dictionary(tweet):
  text = tweet['text']
  sanitized_text = sanitize_tweet(text)

  word_groups = get_word_groups(sanitized_text)

  for word_group in word_groups:
    save_word_group(word_group)
