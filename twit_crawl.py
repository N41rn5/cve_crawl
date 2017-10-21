'''
	Crawl CVEnew Twitter
'''

import tweepy
import os
import time
import datetime
import cve_crawl

base_dir = os.path.dirname(os.path.abspath(__file__))


#---------------------------------------------------------------------------
def twitter_crawler():
	global base_dir

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
	cve_info = api.user_timeline(screen_name="CVEnew", count=10)

# Save Info with folders
	for result in cve_info:

		# Make Folder named with cve number & csv file
		cve_number = result._json["text"].split()[0]
		os.makedirs(base_dir + "\\cve_list\\" + cve_number)
		
		url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cve_number
		cve_data = [["CVE NUMBER", "CVE Description", "CVE URL", "Exploit-DB URL"], cve_crawl.cve_crawler(url)]
		cve_crawl.csv_writer(cve_data, cve_number)


#-------------------------------------------------------------------------------
if __name__ == "__main__":
	
	while(1):
		twitter_crawler()

		print("Path is created at ", end="")
		now_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		print(now_date_time)
		
		# Loop Forever!
		time.sleep(300)


# TODO : Save Info with mongodb
# 옵션에 따라 파일로할지 몽고로 할지 결정