import os
from django.http import FileResponse
from urllib.parse import urlparse
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_resources_csv_file(resources):
    resources_for_csv = list()
    for resource in resources:
        resources_for_csv.append({
            'Target': resource['Target'], 
            'Subdomain': resource['Subdomain'],
            'IP': resource['IP'], 
            'ASN': resource['ASN'],
            'ISP': resource['ISP'],
            'Organization': resource['Organization'], 
            'Country': resource['Country'],
            'Region': resource['Region'], 
            'City': resource['City'],
            'Latitude': resource['Latitude'],
            'Longuitude': resource['Longuitude'], 
            'TimeZone': resource['TimeZone'], 
            'User': resource['User']
        })
    df = pd.DataFrame(resources_for_csv)

    df.to_csv('test.csv',  index=False, encoding='utf-8')
    return FileResponse(open('test.csv', 'rb'))