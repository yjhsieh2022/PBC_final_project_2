
import urllib.request
import json
import datetime
from googlemaps import convert

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = ''  # 因為github是公開的所以上傳的時候要記得刪掉金鑰喔!
origin = input('Where are you?').replace(' ', '+')
destination = input('where do you want to go?').replace(' ', '+')
year = int(input('Enter a year'))
month = int(input('Enter a month'))
day = int(input('Enter a day'))
hour = int(input('Enter a hour'))
minutes = int(input('Enter a minute'))
dep_time = datetime.datetime(year, month, day, hour, minutes)
dep_time = convert.time(dep_time)

# 在主url後加上路徑的url
nav_request = 'origin={}&destination={}&key={}&departure_time={}&mode=transit&language=zh-TW'.format(origin, destination, api_key, dep_time)
request = endpoint + nav_request
print(request)

response = urllib.request.urlopen(request).read()  # 讀進路徑程式碼
directions = json.loads(response.decode('utf-8'))  # 將java資訊轉換為python可讀的型態
print(directions)

if directions['status'] == 'ZERO_RESULTS':
    print('I found no route.')#結果顯示找不到路徑

else:
    transport_means = []
    steps = directions['routes'][0]['legs'][0]['steps']  # route路徑/legs每個路徑中的各交通方式/steps各交通方式的詳細資訊
    for item in steps:
        if item['travel_mode'] == 'TRANSIT':  # transit為選擇大眾運輸工具
            transport_info = []
            transport_info.append(item['transit_details']['line']['vehicle']['type'])  # 交通工具
            transport_info.append(item['transit_details']['line']['short_name'])  # 路線編碼
            transport_info.append(item['transit_details']['departure_stop']['name'])  # 起點站名
            transport_info.append(item['transit_details']['arrival_stop']['name'])  # 終點站名
            transport_info.append(item['transit_details']['departure_time']['value'])  # 以秒計的時間戳
            
            transport_means.append(transport_info)

    print(transport_means)