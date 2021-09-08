from re import split
import sys
import requests
import json
import socket
import time
from pymongo import MongoClient
from datetime import datetime

# Then we set the target and api key from cli
target = sys.argv[1]
api_key = sys.argv[2]
projectname = sys.argv[3]
username = sys.argv[4]

## For Mongo DB
# Making Connection
myclient = MongoClient("mongodb://192.168.88.131:27017/") 
   
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
            'Country Code': country_code, 
            'Region': region_name, 
            'Region Code': region, 
            'City': city, 
            'ZIP Code': zip_code, 
            'Latitude': lat, 
            'Longuitude': lon, 
            'TimeZone': timezone, 
            'Project Name': projectname, 
            'User': username,
            'date_found': timestamp,
            'last_seen': timestamp
            }

    exist = Collection.find_one({'Target': host_data['Target'], 'Subdomain': host_data['Subdomain']})
    if not exist:
        Collection.insert_one(host_data)
        print(subdomain)
    else:
        Collection.update_one({'_id': exist.get('_id')},
         {'$set': 
            {
            'last_seen': timestamp
            }})
        print("Updating subdomain last seen date")

   
print(f"Total subdomains found against {target}: {total_subdomains}")    
