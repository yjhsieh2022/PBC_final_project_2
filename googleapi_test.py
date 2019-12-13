
import urllib.request
import json
import datetime
from googlemaps import convert

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = ''
origin = input('Where are you?').replace(' ', '+')
destination = input('where do you want to go?').replace(' ', '+')
year = int(input('Enter a year'))
month = int(input('Enter a month'))
day = int(input('Enter a day'))
hour = int(input('Enter a hour'))
minutes = int(input('Enter a minute'))
dep_time = datetime.datetime(year, month, day, hour, minutes)
dep_time = convert.time(dep_time)

nav_request = 'origin={}&destination={}&key={}&departure_time={}&mode=transit&language=zh-TW'.format(origin, destination, api_key, dep_time)
request = endpoint + nav_request
print(request)

response = urllib.request.urlopen(request).read()
directions = json.loads(response.decode('utf-8'))
print(directions)

transport_means = []
steps = directions['routes'][0]['legs'][0]['steps']
for item in steps:
    if item['travel_mode'] == 'TRANSIT':
        transport_info = []
        transport_info.append(item['transit_details']['line']['vehicle']['type'])
        transport_info.append(item['transit_details']['line']['short_name'])
        transport_info.append(item['transit_details']['departure_stop']['name'])
        transport_info.append(item['transit_details']['arrival_stop']['name'])
        transport_info.append(item['transit_details']['departure_time']['value'])
        
        transport_means.append(transport_info)

print(transport_means)
