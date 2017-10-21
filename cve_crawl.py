'''
	CVE LIST CRAWLER
'''

from bs4 import BeautifulSoup as BS
import urllib.request as ulib
import os
import time
import csv

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

	data = ulib.urlopen(url).read()
	soup = BS(data, "html.parser")
	result_data = []

	letters = soup.find_all("div", id="GeneratedTable")

	cnt = 1
	end = True
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
			elif end:
				end = False
				result_data.append("No Exploit-DB")

		print(result_data)
		return result_data



#------------------------------------------------------------------------------
if __name__ == "__main__":

	for cnum in cve_lists:
		url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cnum
		cve_data = [["CVE NUMBER", "CVE Description", "CVE URL", "Exploit-DB URL"], cve_crawler(url)]
		csv_writer(cve_data, cnum)

		time.sleep(1)



#TODO : SAVE INFO AS EXCEL / MONGODB
# ebd_url 추출했음 / cve number / cve description / cve url 추출했음 / exploit code랑 프로그램 추출못했음
