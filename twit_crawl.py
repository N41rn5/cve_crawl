'''
	Crawl CVEnew Twitter
'''

import tweepy
import os
import time
import datetime

while(1) :

	# Access Info of my tweeter app
	consumer_key = "zoBCXhFflD1YxkzamVUZjfCko"
	consumer_secrete = "TopBySxKK6CLKDMW2Y4ybHFMXzfYtKJZkpIyHAQySBX8UPx9jh"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secrete)


	# Access Token
	access_token = 	"920568166945656832-9NGjIEft7ulMcvseK1mzwFmpDSAnXXW"
	access_token_sec = "9NgwLI52H8TRFwijogklVEI4Rz4K1BjGOho6Kvd7QGHs9"

	auth.set_access_token(access_token, access_token_sec)


	# Make tweepy API
	api = tweepy.API(auth)

	# Get Timeline info of "CVEnew" with json
	cve_info = api.user_timeline(screen_name="CVEnew", count=200)

	for result in cve_info:

		# Make Folder named with cve number
		cve_number = result._json["text"].split()[0]
		os.makedirs("C:\\Users\\Namjo\\Desktop\\workspace\\cve_crawl\\cve_list\\"+cve_number, exist_ok=True)
		
	print("Path is created at ", end="")
	
	now_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print(now_date_time)
	
	# Loop Forever!
	time.sleep(5)
