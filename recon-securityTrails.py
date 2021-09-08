from re import split
import sys
import requests
import json
import socket
import time
from pymongo import MongoClient
from datetime import datetime
import argparse

print("   __    ___  __  __       ____  ____   ___  _____  _  _ ")
print("  /__\  / __)(  \/  ) ___ (  _ \( ___) / __)(  _  )( \( )")
print(" /(__)\ \__ \ )    ( (___) )   / )__) ( (__  )(_)(  )  ( ")
print("(__)(__)(___/(_/\/\_)     (_)\_)(____) \___)(_____)(_)\_)")
print("                                                         ")
print("--------------Subdomain Reconnaissance Tool--------------")
print("                                                         ")
print("                                                         ")



parser = argparse.ArgumentParser(description='Recon Security Trails to MongoDB')
parser.add_argument('-d', '--domain', help='Domain to scan')
parser.add_argument('-A', '--api', help='Security Trails API-KEY')
parser.add_argument('-p', '--project', help='The name of the project, this name will be the collection name on MongoDB')
parser.add_argument('-u', '--user', help='The username to make a DB on mongo and save your recon data')
parser.add_argument('-m', '--mongodb', help='The MongoDB connection string. Example: mongodb://127.0.0.1:27017/')

args = parser.parse_args()

target = args.domain
api_key = args.api
projectname = args.project
username = args.user
mongodb = args.mongodb

## For Mongo DB
# Making Connection
myclient = MongoClient(mongodb) 
   
# database 
db = myclient[username]
   
# Created or Switched to collection 
# names: GeeksForGeeks
Collection = db[projectname]

# First we set the URL of the api
url_api = "https://api.securitytrails.com/v1/domain/"

# The request type is the path to te api before the taget on the URL
request_type = "/subdomains"

# Then concatenate the url to send the request to the api
url = url_api + target + request_type

querystring = {"children_only":"false","include_inactive":"true"}

# We pass the api key from cli to headers
headers = {
    "Accept": "application/json",
    "APIKEY": api_key
}

# Make the rreuqest
response = requests.request("GET", url, headers=headers, params=querystring)

# Transform response into json_data
json_data = json.loads(response.text)

subdomains = json_data["subdomains"]

try:
    total_subdomains = json_data["subdomain_count"]
except:
    print("No results, founded")

for sub in subdomains:
    subdomain = (sub + "." + target) 
    time.sleep(0.01)
    try:
        IP_addres = socket.gethostbyname(subdomain)
    except: 
        IP_addres = "Null"
        pass
    
    for ip in subdomain:
        ip = IP_addres
        time.sleep(2)
    
        additional_information = requests.get('http://ip-api.com/json/' + ip, verify=False)

        try:
            json_adinfo = json.loads(additional_information.text)
        except:
            pass
        if json_adinfo != "NULL":
            try:
                country = json_adinfo['country']
            except:
                country = "Null"
                pass
        
            try:
                country_code = json_adinfo['countryCode']
            except:
                country_code = "Null"
                pass
          
            try:
                region = json_adinfo['region']
            except:
                region = "Null"
                pass
            
            try:
                region_name = json_adinfo['regionName']
            except:
                region_name = "Null"
                pass

            try:
                city = json_adinfo['city']
            except:
                city = "Null"
                pass

            try:
                zip_code = json_adinfo['zip']
            except:
                zip_code = "Null"
                pass

            try:
                lat = json_adinfo['lat']
            except:
                lat = "Null"
                pass

            try:
                lon = json_adinfo['lon']
            except:
                lon = "Null"
                pass

            try:
                timezone = json_adinfo['timezone']
            except:
                timezone = "Null"
                pass

            try:
                isp = json_adinfo['isp']
            except:
                isp = "Null"
                pass
         
            try:
                org = json_adinfo['org']
            except:
                org = "Null"
                pass

            try:
                asn = json_adinfo['as']
            except:
                asn = "Null"
                pass
        else:
            pass
        
        timestamp = datetime.now()

        host_data = {
            'Target': target, 
            'Subdomain': subdomain, 
            'IP': ip, 
            'ASN': asn, 
            'ISP': isp, 
            'Organization': org, 
            'Country': country, 
            'Country_Code': country_code, 
            'Region': region_name, 
            'Region_Code': region, 
            'City': city, 
            'ZIP_Code': zip_code, 
            'Latitude': lat, 
            'Longuitude': lon, 
            'TimeZone': timezone, 
            'Project_Name': projectname, 
            'User': username,
            'date_found': timestamp,
            'last_seen': timestamp
            }

    exist = Collection.find_one({'Target': host_data['Target'], 'Subdomain': host_data['Subdomain']})
    if not exist:
        Collection.insert_one(host_data)
        print(f"Subdomain found: {subdomain}")
    else:
        Collection.update_one({'_id': exist.get('_id')},
         {'$set': 
            {
            'last_seen': timestamp
            }})
        print(f"Updating subdomain {subdomain} last seen date: {timestamp}")

   
print(f"Total subdomains found against {target}: {total_subdomains}")
print(f"Results added to Mongodb {mongodb}, DB Name: {username}, and Collection {projectname}")
