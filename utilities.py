import binascii

def to_file_name(text):
  return binascii.hexlify(text.encode()).decode('utf-8')

def from_file_name():
  return binascii.unhexlify(file_name).decode('utf-8')

def end_of_tweet_marker():
  return 'END OF TWEET'