import tweepy
import qanon as Q
import time
import pickle
import markovify
import yaml

CONFIG = yaml.safe_load(open("config.yml", "r"))

auth = tweepy.OAuthHandler(CONFIG["consumer_key"], CONFIG["consumer_secret"])
auth.set_access_token(CONFIG["access_token"], CONFIG["access_token_secret"])

api = tweepy.API(auth)

def load_markov():
	return pickle.loads(open("markovchain.p", "rb").read())

def save_markov(chain):
	open("markovchain.p", "wb").write(pickle.dumps(chain))

def generate_tweet(CHAIN):
	return CHAIN.make_short_sentence(CONFIG["max_characters"])

def tweet(text):
	print(f"Tweeting: {text}")
	api.update_status(text)

print("Loading saved markov chain...")
try:
	MARKOV = load_markov()
	print("Markov chain loaded.")
except FileNotFoundError:
	print("No saved markov chain found. Generating now.")
	MARKOV = markovify.Text(Q.QDropListToText(Q.DROPCACHE))
	print("Markov chain generated. Saving...")
	save_markov(MARKOV)
	print("Markov chain saved.")

while True:
	time.sleep(CONFIG["wait_time"])
	new_ones = Q.get_new_drops()
	if len(new_ones) > 3:
		MARKOV = markovify.combine([MARKOV, markovify.Text(new_ones)])
		save_markov(MARKOV)
	tweet(generate_tweet(MARKOV))
	
