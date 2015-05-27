import tweepy
import cPickle as pickle
import os.path
from gtts import gTTS
import subprocess

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')

api = tweepy.API(auth)

if os.path.exists('last_id.p'): #check for pickle, retrieve last tweet id, get tweets
	last_id = pickle.load(open("last_id.p","rb"))
	mentions = api.mentions_timeline(since_id = last_id)
else: #no pickle exists, just get last 3 tweets
	mentions = api.mentions_timeline(count = 3)

if mentions: 
	pickle.dump(mentions[0].id,open("last_id.p","wb")) #dump newest id
	speech=[]
	

	for mention in mentions: #process tweets into readable form
		line =  mention.user.screen_name+' says '+mention.text.replace('@EEELevel5Labs','')
		speech.append(line)
		print(line)

		api.retweet(mention.id) #retweet


	speech = '...'.join(speech)

	ts = gTTS(text=speech, lang='en')
	ts.save('twits.mp3')

	

	try:
		subprocess.call(['cvlc', '--play-and-exit', '--volume', '500', 'twits'])
	except OSError:
		subprocess.call(['mpg123', 'twits.mp3'])


else:
	print 'no new tweets'
