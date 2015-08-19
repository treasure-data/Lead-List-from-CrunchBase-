import urllib2
import json
import csv
import codecs
import time


uuid_counter = 0
error_counter =0
records_scanned =1

def get_uuid():	
	print "Accessing the organisations"
	has_next_page = True;
	page = 1
	while(has_next_page):
		url = "https://api.crunchbase.com/v/3/organizations?page=%s&user_key=419d2896eaa2ef4a93bff62ae0af51e8"%page
		url_data = urllib2.urlopen(url)
		json_obj = json.load(url_data)
		json_data = json_obj["data"]
		total_no_pages = json_data["paging"]["number_of_pages"]
		json_items = json_data["items"]
		for item in json_items:
			csv_row=[]
			csv_row.append(item["properties"]["name"])
			company_type = item["properties"]["primary_role"]
			website = item["properties"]["homepage_url"]
			csv_row.append(website)
			csv_row.append(item["properties"]["linkedin_url"])
			csv_row.append(item["properties"]["country_code"])
			global records_scanned
			print "Total Records Scanned:%d" %records_scanned
			records_scanned += 1
			if company_type =="company" and website !=None:
				uuid=item["uuid"]
				series_qualifier(uuid,csv_row)
		page += 1
		if page > 37:
			has_next_page = False
		
			#get_info(x,name,website,linkedin,country)


def series_qualifier(uuid,csv_row):
	
	global uuid_counter
	url = "https://api.crunchbase.com/v/3/funding-rounds/%s?user_key=419d2896eaa2ef4a93bff62ae0af51e8"%uuid
	uuid_counter = uuid_counter + 1
	#time.sleep(7)
	try:
		url_data = urllib2.urlopen(url)
		json_obj = json.load(url_data)
		if json_obj["data"]["relationships"].has_key("funding_rounds"):
			if json_obj["data"]["relationships"]["funding_rounds"].has_key("items"):
				funding_rounds_items = json_obj["data"]["relationships"]["funding_rounds"]["items"]
				for item in funding_rounds_items:
					if item.has_key("properties"):
						properties = item["properties"]
						if properties.has_key("series"):
							series_values = properties["series"]
							if series_values in ["C", "D", "E"]:
								break;
							if series_values == "B":
								print "series qualified record found!"
								get_info(uuid,csv_row)
	except urllib2.HTTPError:
		'''with open('error.txt', 'a') as filehandle:
			filehandle=str(filehandle)
			filehandle.write(url)'''	
		global error_counter 
		print "Error Number:%d" %error_counter
	 	error_counter +=1



def get_info(uuid,csv_row):
	
	url = "https://api.crunchbase.com/v/3/funding-rounds/%s?user_key=419d2896eaa2ef4a93bff62ae0af51e8"%uuid
	url_data = urllib2.urlopen(url)
	json_obj = json.load(url_data)
	founder =[]	
	category=[]
	#category_keywords= ["Apps", "Games","Dating","Mobile","Marketing","Internet of Things","Retail","E-commerce","Software","Analytics","SaaS", "Device", "Data", "Transport", "Online Games", "Wearable Devices", "Cab", "iOS", "Google", "Watch", "IoT", "Big", "Internet", "Things"]
	if json_obj["data"]["relationships"].has_key("categories"):
		category_items = json_obj["data"]["relationships"]["categories"]["items"]
		for cat_item in category_items:
			if cat_item.has_key("properties"):
				category.append(cat_item["properties"]["name"])
	if json_obj["data"]["relationships"].has_key("founders"):
		founder_items = json_obj["data"]["relationships"]["founders"]["items"]
		for founder_item in founder_items:
			if founder_item.has_key("properties"):
				founder.append(founder_item["properties"]["first_name"] +" "+ founder_item["properties"]["last_name"])
	csv_row.insert(-1, founder)
	csv_row.insert(-1, category)
	print "Printing a new record"
	write_to_csv(csv_row)
	
		
#name, website,linkedin,category,founder,country

def write_to_csv(row):
	try:
		with open('testfile.csv', 'a') as csvfile:
			writer= csv.writer(csvfile, delimiter= ',')
			writer.writerow(row)
	except UnicodeEncodeError:
		print row[0] + " " + row[1] 

									
get_uuid()

