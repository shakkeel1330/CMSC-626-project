import geoip2.database

"""
reader = geoip2.database.Reader('./GeoLite2-City_20190430/GeoLite2-City.mmdb')

response = reader.city('10.0.0.148')

print(response.country.iso_code)
print(response.country.name)
print(response.country.names['zh-CN'])
print(response.subdivisions.most_specific.name)
print(response.subdivisions.most_specific.iso_code)
print(response.city.name)
print(response.postal.code)
print(response.location.latitude)
print(response.location.longitude)

reader.close()

import requests
import json

# IP address to test
ip_address = '10.200.146.213'

# URL to send the request to
request_url = 'https://geolocation-db.com/jsonp/' + ip_address
# Send request and decode the result
response = requests.get(request_url)
result = response.content.decode()
# Clean the returned string so it just contains the dictionary data for the IP address
result = result.split("(")[1].strip(")")
# Convert this data into a dictionary
result  = json.loads(result)
print(result)
"""
from ip2geotools.databases.noncommercial import DbIpCity
response = DbIpCity.get('10.0.0.148', api_key='free')
print(response.city)