'''
	read cve_allitems.csv and parse it
'''

import csv
import os
import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
allitems_dir = base_dir+"\\cve_allitems.csv"


#------------------------------------------------------------------
def make_dir():
	global base_dir
	global allitems_dir

	with open(allitems_dir, "r", encoding="ISO-8859-1") as csvfile:
		read_csv = csv.reader(csvfile, delimiter=",")

		for row in read_csv:

			if row[0][:4] != "CVE-":
				continue
			else:
				if int(row[0][4:8]) < 2011:
					continue

			os.makedirs(base_dir + "\\cve_list\\" + row[0], exist_ok=True)

	print("Path is created at ", end="")
	
	now_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print(now_date_time)




# TODO : SAVE INFO AS FILE / MONGODB
