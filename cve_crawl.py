'''
	CVE LIST CRAWLER
'''

from bs4 import BeautifulSoup as BS
from urllib.request import urlopen, Request, urlretrieve
import os
import time
import csv
import random
import re

user_agent_list = [
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
             "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
             "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
             "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
             "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
             "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
             "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
             "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]

base_dir = os.path.dirname(os.path.abspath(__file__))
cve_lists = os.listdir(base_dir + "\\cve_list")

def csv_writer(data, cve_number):

	global base_dir

	with open(base_dir + "\\cve_list\\" + cve_number + "\\" + cve_number + ".csv", "w", newline="\n") as csvfile:
		writer = csv.writer(csvfile, delimiter=",")
		for line in data:
			writer.writerow(line)

#--------------------------------------------------------------------------------------------------------------
def cve_crawler(url):

	data = urlopen(Request(url)).read()
	soup = BS(data, "html.parser")
	result_data = []

	letters = soup.find_all("div", id="GeneratedTable")

	cnt = 0
	for result in letters:

		cve_number = result.contents[1].find_all("td")[0].get_text().replace("\n", "")
		cve_desc = result.contents[1].find_all("td")[2].get_text().replace("\n", "")
		result_data.append(cve_number)
		result_data.append(cve_desc)
		result_data.append(url)

		for ref in result.contents[1].find_all("td")[4].get_text().strip().split("\n"):
			
			if "exploit-db" in ref:
				edb_url = soup.find("a", text=ref)['href']
				result_data.append(edb_url)
				edb_data = edb_crwal(cve_number, edb_url)

				for data in edb_data:
					result_data.append(data)

				cnt = cnt + 1

		if cnt == 0:
			result_data.append("No Exploit-DB")

		print(result_data)
		return result_data

#------------------------------------------------------------------------------
def edb_crwal(cve_number, url):

	global user_agent_list

	user_agent = random.choice(user_agent_list)
	headers = {'User-Agent' : user_agent}
	data = urlopen(Request(url, None, headers= headers)).read()
	soup = BS(data, "html.parser", from_encoding="ISO-8859-1")

	platform = soup.find("a", href=re.compile("www.exploit-db.com/platform")).text
	ttype = soup.find("strong", text="Type").next_sibling.next_sibling.text
	exploit = soup.find("a", href=re.compile("www.exploit-db.com/download"))['href']
	
	if exploit != None:
		urlretrieve(exploit, base_dir + "\\cve_list\\" + cve_number + "\\" + cve_number + "_exploit.txt")

	return [platform, ttype, exploit]

#------------------------------------------------------------------------------
if __name__ == "__main__":

	for cnum in cve_lists:
		url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cnum
		cve_data = [
			[
				"CVE NUMBER", "CVE Description", "CVE URL", "Exploit-DB URL",
				"Exploit Platform", "Exploit Type", "Exploit Code"
			], 
			cve_crawler(url)
		]
		# json으로 map - mongodb
		csv_writer(cve_data, cnum)

		time.sleep(1)


#TODO : SAVE INFO AS EXCEL / MONGODB
# 프로그램 추출못했음
