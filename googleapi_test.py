
import urllib.request
import json
import datetime
from googlemaps import convert
from urllib.parse import quote

class GoogleAPI:
    def get_bus_full_price(origin, destination, year, month, day, hour, minutes):
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        api_key = ''
        '''
        origin = input('Where are you?')
        destination = input('where do you want to go?')
        year = int(input('Enter a year: '))
        month = int(input('Enter a month: '))
        day = int(input('Enter a day: '))
        hour = int(input('Enter a hour: '))
        minutes = int(input('Enter a minute: '))
        '''
        dep_time = datetime.datetime(year, month, day, hour, minutes)
        dep_time = convert.time(dep_time)

        nav_request = 'origin={}&destination={}&key={}&departure_time={}&mode=transit&transit_mode=bus&language=zh-TW'.format(quote(origin), quote(destination), api_key, dep_time)
        request = endpoint + nav_request
        #print(request)

        response = urllib.request.urlopen(request).read()
        directions = json.loads(response.decode('utf-8'))
        #print(directions)

        fare = directions['routes'][0]['fare']['text']
        return fare

    def get_transport_info(origin, destination, year, month, day, hour, minutes):
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        api_key = 'AIzaSyBWzsLj0BrvJ_05uu7MAJZ-A93NOp_U970'
        '''
        origin = input('Where are you?')
        destination = input('where do you want to go?')
        year = int(input('Enter a year: '))
        month = int(input('Enter a month: '))
        day = int(input('Enter a day: '))
        hour = int(input('Enter a hour: '))
        minutes = int(input('Enter a minute: '))
        '''
        dep_time = datetime.datetime(year, month, day, hour, minutes)
        dep_time = convert.time(dep_time)

        nav_request = 'origin={}&destination={}&key={}&departure_time={}&mode=transit&avoid=ferries&language=zh-TW&alternatives=true'.format(quote(origin), quote(destination), api_key, dep_time)
        request = endpoint + nav_request
        #print(request)

        response = urllib.request.urlopen(request).read()
        directions = json.loads(response.decode('utf-8'))
        #print(directions)

        routes_list = []
        #print(len(directions['routes'][0]['legs'][0]['steps']))
        for k in range(len(directions['routes'])):
            for i in range(len(directions['routes'][k]['legs'])):
                leg = directions['routes'][k]['legs'][i]['steps']
                #print(leg)
                #print('======')
                routes_list.append(leg)

        means_list = []
        if directions['status'] == 'ZERO_RESULTS':
            print('I found no route.')  # 結果顯示找不到路徑
        else:
            for i in range(len(routes_list)):
                transport_means = []
                for item in routes_list[i]:
                    if item['travel_mode'] == 'TRANSIT':
                        if item['transit_details']['line']['vehicle']['type'] == 'BUS':  # 路線編號 起站 訖站
                            transport_info = []
                            transport_info.append(item['transit_details']['line']['vehicle']['type'])
                            transport_info.append(item['transit_details']['line']['short_name'])
                            transport_info.append(item['transit_details']['departure_stop']['name'])
                            transport_info.append(item['transit_details']['arrival_stop']['name'])
                            departure_date_info = datetime.datetime.fromtimestamp(item['transit_details']['departure_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                            transport_info.append(departure_date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                            transport_info.append(item['transit_details']['departure_time']['text'])
                            arrival_date_info = datetime.datetime.fromtimestamp(item['transit_details']['arrival_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                            transport_info.append(arrival_date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                            transport_info.append(item['transit_details']['arrival_time']['text'])
                            time = item['transit_details']['departure_time']['text'].split(':')
                            dep_hour = time[0][2:]
                            dep_minute = time[1]
                            fare = GoogleAPI.get_bus_full_price(item['transit_details']['departure_stop']['name'], item['transit_details']['arrival_stop']['name'], year = int(year), month = int(month), day = int(day), hour = int(dep_hour), minutes = int(dep_minute))
                            transport_info.append(fare)
                            transport_means.append(transport_info)
                        elif item['transit_details']['line']['vehicle']['type'] == 'HEAVY_RAIL':  # 高鐵/台鐵
                            if item['transit_details']['line']['short_name'] == '高鐵':  # 高鐵  日期 格式是2019/12/13 起站 訖站 車次號碼
                                transport_info = []
                                transport_info.append(item['transit_details']['line']['vehicle']['type'])
                                transport_info.append(item['transit_details']['line']['short_name'])
                                transport_info.append(item['transit_details']['trip_short_name'])
                                transport_info.append(item['transit_details']['departure_stop']['name'])
                                transport_info.append(item['transit_details']['arrival_stop']['name'])
                                date_info = datetime.datetime.fromtimestamp(item['transit_details']['departure_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                                transport_info.append(date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                                transport_info.append(item['transit_details']['departure_time']['text'])
                                date_info = datetime.datetime.fromtimestamp(item['transit_details']['arrival_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                                transport_info.append(date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                                transport_info.append(item['transit_details']['arrival_time']['text'])
                                transport_means.append(transport_info)
                            else:  # 台鐵 車次 起站 訖站 時間
                                transport_info = []
                                transport_info.append(item['transit_details']['line']['vehicle']['type'])
                                transport_info.append(item['transit_details']['line']['short_name'])
                                transport_info.append(item['transit_details']['trip_short_name'])
                                transport_info.append(item['transit_details']['departure_stop']['name'])
                                transport_info.append(item['transit_details']['arrival_stop']['name'])
                                date_info = datetime.datetime.fromtimestamp(item['transit_details']['departure_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                                transport_info.append(date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                                transport_info.append(item['transit_details']['departure_time']['text'])
                                date_info = datetime.datetime.fromtimestamp(item['transit_details']['departure_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                                transport_info.append(date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數
                                transport_info.append(item['transit_details']['arrival_time']['text'])
                                transport_means.append(transport_info)
                means_list.append(transport_means)

        return means_list

print(GoogleAPI.get_transport_info('北投', '九份', 2019, 12, 20, 11, 30))