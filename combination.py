
import urllib.request
import json
import datetime
from googlemaps import convert
from urllib.parse import quote
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

class GoogleAPI:
    def get_bus_full_price(origin, destination, year, month, day, hour, minutes):
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        api_key = 'AIzaSyBWzsLj0BrvJ_05uu7MAJZ-A93NOp_U970'

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

        dep_time = datetime.datetime(year, month, day, hour, minutes)
        dep_time = convert.time(dep_time)

        # 子url 限定大眾交通工具(除了航運)、中文輸入輸出、多條路線
        nav_request = 'origin={}&destination={}&key={}&departure_time={}&mode=transit&avoid=ferries&language=zh-TW&alternatives=true'.format(quote(origin), quote(destination), api_key, dep_time)
        request = endpoint + nav_request

        response = urllib.request.urlopen(request).read()  # 讀進google api吐出的內容
        directions = json.loads(response.decode('utf-8'))  # 用json整理資訊

        routes_list = []
        #print(len(directions['routes'][0]['legs'][0]['steps']))
        for k in range(len(directions['routes'])):  # 分出路線
            for i in range(len(directions['routes'][k]['legs'])):  # 分出個別交通方式
                leg = directions['routes'][k]['legs'][i]['steps']
                routes_list.append(leg)

        means_list = []
        if directions['status'] == 'ZERO_RESULTS':
            print('I found no route.')  # 結果顯示找不到路徑
        else:
            for i in range(len(routes_list)):
                transport_means = []  # 單一路線的詳細資訊
                for item in routes_list[i]:  # 個別交通方式的資訊
                    if item['travel_mode'] == 'TRANSIT':
                        if item['transit_details']['line']['vehicle']['type'] == 'BUS':  # 路線編號 起站 訖站
                            transport_info = []
                            transport_info.append(item['transit_details']['line']['vehicle']['type'])  # BUS
                            transport_info.append(item['transit_details']['line']['short_name'])  # 路線編號
                            transport_info.append(item['transit_details']['departure_stop']['name'])  # 起站名
                            transport_info.append(item['transit_details']['arrival_stop']['name'])  # 訖站名
                            departure_date_info = datetime.datetime.fromtimestamp(item['transit_details']['departure_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                            transport_info.append(departure_date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                            transport_info.append(item['transit_details']['departure_time']['text'])  #上午/下午00:00
                            arrival_date_info = datetime.datetime.fromtimestamp(item['transit_details']['arrival_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                            transport_info.append(arrival_date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                            transport_info.append(item['transit_details']['arrival_time']['text'])  # 上午/下午00:00
                            time = item['transit_details']['departure_time']['text'].split(':')
                            dep_hour = time[0][2:]
                            dep_minute = time[1]
                            fare = GoogleAPI.get_bus_full_price(item['transit_details']['departure_stop']['name'], item['transit_details']['arrival_stop']['name'], year = int(year), month = int(month), day = int(day), hour = int(dep_hour), minutes = int(dep_minute))
                            transport_info.append(fare)  # 全票票價(用來抓半票票價)
                            transport_means.append(transport_info)
                        elif item['transit_details']['line']['vehicle']['type'] == 'HEAVY_RAIL':  # 高鐵/台鐵
                            if item['transit_details']['line']['short_name'] == '高鐵':  # 高鐵  日期 格式是2019/12/13 起站 訖站 車次號碼
                                transport_info = []
                                transport_info.append(item['transit_details']['line']['vehicle']['type'])  # HEAVY_RAIL
                                transport_info.append(item['transit_details']['line']['short_name'])  # 高鐵
                                transport_info.append(item['transit_details']['trip_short_name'])  # 編號
                                transport_info.append(item['transit_details']['departure_stop']['name'])  # 起站名
                                transport_info.append(item['transit_details']['arrival_stop']['name'])  # 訖站名
                                date_info = datetime.datetime.fromtimestamp(item['transit_details']['departure_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                                transport_info.append(date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                                transport_info.append(item['transit_details']['departure_time']['text'])  # 上午/下午00:00
                                date_info = datetime.datetime.fromtimestamp(item['transit_details']['arrival_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                                transport_info.append(date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                                transport_info.append(item['transit_details']['arrival_time']['text'])  # 上午/下午00:00
                                transport_means.append(transport_info)
                            else:  # 台鐵 車次 起站 訖站 時間
                                transport_info = []
                                transport_info.append(item['transit_details']['line']['vehicle']['type'])  # HEAVY_RAIL
                                transport_info.append(item['transit_details']['line']['short_name'])  # 車種
                                transport_info.append(item['transit_details']['trip_short_name'])  # 車次
                                transport_info.append(item['transit_details']['departure_stop']['name'])  # 起站名
                                transport_info.append(item['transit_details']['arrival_stop']['name'])  # 訖站名
                                date_info = datetime.datetime.fromtimestamp(item['transit_details']['departure_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                                transport_info.append(date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數)
                                transport_info.append(item['transit_details']['departure_time']['text'])  # 上午/下午00:00
                                date_info = datetime.datetime.fromtimestamp(item['transit_details']['departure_time']['value'])  # 從UTC格式(秒)轉成datetime格式
                                transport_info.append(date_info.strftime('%Y/%m/%d'))     # 2019/12/05 //23:00(高鐵，日期，時間分兩個變數
                                transport_info.append(item['transit_details']['arrival_time']['text'])  # 上午/下午00:00
                                transport_means.append(transport_info)
                means_list.append(transport_means)

        return means_list  # 各路線中交通方式的詳細資訊

# print(GoogleAPI.get_transport_info('台北', '高雄', 2019, 12, 20, 11, 30))

class GetTicketPrice:

    def Bus(num_route, full_ticket_price):
        '''
        num_route = input(路線編號:)
        data_pickedroute = '0_,' + str(num_route) + '_,0'
        full_ticket_price = input(全票價格:)
        ticket_type = input(全票輸入1,半票輸入0:)
        '''
        if 48 <= ord(num_route[0]) <= 57:
            data_pickedroute = '0_,' + str(num_route) + '_,0'
        else:
            return None
        '''找到填入url的代號'''
        data_topost = {'Type':'GetKey', 'Data':data_pickedroute, 'Lang':'#'}
        r_route = requests.post('https://www.taiwanbus.tw/APP_API/Test/ByLine.aspx', data=data_topost, verify=False)
        R_Route = [ r.strip('_') for r in r_route.text.split(',')]

        '''填入代號連到價格頁面'''
        url_price_page = 'https://web.taiwanbus.tw/eBUS/subsystem/ticket/TMSquery.aspx?run_id=' + str(R_Route[4])  # 這裡是採用去程:R[4]；如果回程:R[9]
        driver_price_page = webdriver.Chrome(executable_path ='C:\\Users\\linda\\Downloads\\chromedriver_win32\\chromedriver.exe')
        driver_price_page.get(url_price_page)

        html_price_page = driver_price_page.page_source
        # driver_price_page.close()  # 先不關

        soup_price_page = BeautifulSoup(html_price_page, 'html.parser')
        attr_price_page = {'valign':'middle'}
        price_tags = soup_price_page.find_all('td', attrs=attr_price_page)
        price_list = []
        for tag in price_tags:
            price_list.append(tag.get_text())

        price_len = len(price_list)//2  # 將全票半票資訊分開
        full_price_list = price_list[:price_len]
        half_price_list = price_list[price_len:]

        stop_number = [0]  # 站名的index list
        number = 0
        for i in range(2,20):
            number += i
            stop_number.append(number)
        # print(stop_number)

        stop_list = []  # 站名list
        full_price_tri_list = []  # 全票價格
        for i in full_price_list:
            if full_price_list.index(i) in stop_number:
                stop_list.append(i)
            else:
                full_price_tri_list.append(i)
        half_price_tri_list = []  # 半票價格
        for i in half_price_list:
            if half_price_list.index(i) not in stop_number:
                half_price_tri_list.append(i)
        # print(stop_list)
        # print(full_price_tri_list)
        # print(half_price_tri_list)
        Full2Half = dict()
        for i in range(len(full_price_tri_list)):
            Full2Half[full_price_tri_list[i]]=half_price_tri_list[i]
        
        half_ticket_price = Full2Half[full_ticket_price]
        Result = [['全票', full_ticket_price],['半票', half_ticket_price]]
        
        return Result

    #print(get_bus_price('1062', '61', '0'))

    def HSHR(StartStation, EndStation, DepartureDate, DepartureTime, TrainNumber):
        
        # google map上的站名和高鐵網站搜尋名不一致
        NameMatch = {   '南港車站':'南港站', 
                        '台北車站':'台北站', 
                        '板橋車站':'板橋站',
                        '高鐵桃園站':'桃園站',
                        '新竹':'新竹站',
                        '高鐵苗栗站':'苗站站',
                        '高鐵台中站':'台中站',
                        '彰化站':'彰化站',
                        '雲林':'雲林站',
                        '嘉義':'嘉義站',
                        '高鐵台南站':'台南站',
                        '新左營站':'左營站'}
        # 將Google Map顯示的站名轉成高官網鐵搜索的站名
        for keys in NameMatch.keys():
            if StartStation == keys:
                StartStation = NameMatch[keys]
            elif EndStation == keys:
                EndStation = NameMatch[keys]
        
        Station = {'南港站':'2f940836-cedc-41ef-8e28-c2336ac8fe68', 
                   '台北站':'977abb69-413a-4ccf-a109-0272c24fd490', 
                   '板橋站':'e6e26e66-7dc1-458f-b2f3-71ce65fdc95f',
                   '桃園站':'fbd828d8-b1da-4b06-a3bd-680cdca4d2cd',
                   '新竹站':'a7a04c89-900b-4798-95a3-c01c455622f4',
                   '苗栗站':'e8fc2123-2aaf-46ff-ad79-51d4002a1ef3',
                   '台中站':'3301e395-46b8-47aa-aa37-139e15708779',
                   '彰化站':'38b8c40b-aef0-4d66-b257-da96ec51620e',
                   '雲林站':'5f4c7bb0-c676-4e39-8d3c-f12fc188ee5f',
                   '嘉義站':'60831846-f0e4-47f6-9b5b-46323ebdcef7',
                   '台南站':'9c5ac6ca-ec89-48f8-aab0-41b738cb1814',
                   '左營站':'f2519629-5973-4d08-913b-479cce78a356'}
        
        # 將google map 12小時制轉24小時制
        if DepartureTime[:2] == '上午':
            if DepartureTime[2:4] == '12':
                DepartureTime = '00'+DepartureTime[4:]
            else:    
                DepartureTime = DepartureTime[2:]
        elif DepartureTime[:2] == '下午':
            if DepartureTime[2:4] == '12':
                DepartureTime = DepartureTime[2:]
            else:
                index = DepartureTime.index(':')
                DepartureTime = str(int(DepartureTime[2:index])+12)+DepartureTime[index:]

        # 高鐵車次號碼首位為1或0，若首位為0，google map會自動省略僅顯示三位數，需手動加零高鐵票價查詢系統爬價格才會對
        if len(TrainNumber) == 3:
            NewTrainNumber = '0' + TrainNumber
        if len(TrainNumber) == 4:
            NewTrainNumber = TrainNumber
        
        # 因為高鐵採用call api獲取json資料的方式，使用requests/selenium都無法在html網頁上直接抓到價格。XHR/Request URL取得真的存有價格的網址，透過requests.post(api)的方式來獲取資料
        url = "http://www.thsrc.com.tw/tw/TimeTable/Search"
        form_data = {
            'StartStation': Station[StartStation],
            'StartStationName': StartStation,
            'EndStation': Station[EndStation],
            'EndStationName': EndStation,
            'DepartueSearchDate': DepartureDate,
            'DepartueSearchTime': DepartureTime,
            'DiscountType': 'e1b4c4d9-98d7-4c8c-9834-e1d2528750f1,68d9fc7b-7330-44c2-962a-74bc47d2ee8a,4baae6e5-b42c-474b-a194-ff8f1783c7bb,40863ff1-a16c-4da1-8af7-c1f8991627f3',
            'SearchType': 'S'
        }

        response_post = requests.post(url, data = form_data)
        data = json.loads(response_post.text)

        """
        data結構：一個字典裡包了兩個小字典：{success}, {data}
        小字典{data}裡包了三個字典：{DepartureTable},
                                    {DestinationTable},
                                    {PriceTable})
        {DepartureTable}裡包了{Title}, {TrainItem}
        {TrainItem}裡包了  {TrainNumber}車次,
                           {DepartureTime}出發時間, 
                           {DestinationTime}抵達時間, 
                           {Duration}行車時間, 
                           {NonReservedCar}自由座車廂數, 
                           {Discount}早鳥/大學生/25人團體/校外教學, 
                           {Note}備註, {Sequence}, 
                           {StationInfo}(這班車停靠哪些站點及時間)
        {PriceTable}裡包了{Coach}(普通車廂）, 
                          {Business}（商務車廂）, 
                          {Unreserved}（自由座）, 
                          {Column}（優惠）
        """

        # 根據車次號碼索引特定一班車，擷取所有優惠，放入字典TrainDiscount中
        TrainDiscount = dict()
        for traininfo in data['data']['DepartureTable']['TrainItem']:
            if traininfo['TrainNumber'] == NewTrainNumber:
                for discount in traininfo['Discount']:
                    TrainDiscount[discount['Name']] = [discount['Value']]
        
        Coach = data['data']['PriceTable']['Coach']
        Business = data['data']['PriceTable']['Business']
        Unreserved = data['data']['PriceTable']['Unreserved']
        
        FullPrice = {'標準車廂':Coach[0],'商務車廂':Business[0],'自由座':Unreserved[0]}
        ChildPrice = {'標準車廂':Coach[1],'商務車廂':Business[1],'自由座':Unreserved[1]}
        """團體票先註解掉
        GroupPrice = {'標準車廂':Coach[2],'商務車廂':Business[2]}  
        """
        ColledgePrice = []
        
        # 將65折起等不確定的折數差成數個準確可對應的折數
        earlybird = {'65折起':['65折','8折','9折'], '8折起':['8折','9折']}
        if '早鳥' in TrainDiscount.keys():
            if TrainDiscount['早鳥'] == ['65折起']:
                TrainDiscount['早鳥'] = earlybird['65折起']
            elif TrainDiscount['早鳥'] == ['8折起']:
                TrainDiscount['早鳥'] = earlybird['8折起']
        """        
        if '校外教學' in TrainDiscount.keys():
            if TrainDiscount['校外教學'] == ['4/7折']:
                TrainDiscount['校外教學'] = ['4折', '7折']
        """
        # 早鳥放入全票類別，如果有大學生自成一類，25人、校外教學放入團體票類別
        if '早鳥' in TrainDiscount.keys():
            for values in TrainDiscount['早鳥']: 
                for Column in data['data']['PriceTable']['Column']:
                    if Column['ColumnName'] == values:
                        FullPrice['早鳥'+Column['ColumnName']] = Column['CoachPrice']                    
        if '大學生' in TrainDiscount.keys():
            for values in TrainDiscount['大學生']: 
                for Column in data['data']['PriceTable']['Column']:
                    if Column['ColumnName'] == values:
                        ColledgePrice = ['大學生'+Column['ColumnName'], Column['CoachPrice']]
        """
        if '25人團體' in TrainDiscount.keys():            
            for values in TrainDiscount['25人團體']: 
                for Column in data['data']['PriceTable']['Column']:
                    if Column['ColumnName'] == values:
                        GroupPrice['25人團體'+Column['ColumnName']] = Column['CoachPrice']
        if '校外教學' in TrainDiscount.keys():
            for values in TrainDiscount['校外教學']:
                for Column in data['data']['PriceTable']['Column']:
                    if Column['ColumnName'] == values:
                        if values == '4折':
                            GroupPrice['小學生校外教學4折'] = Column['CoachPrice']
                        elif values == '7折':
                            GroupPrice['中學、大學生校外教學7折'] = Column['CoachPrice']
        """
        Result = [  ['全票',FullPrice, 'https://irs.thsrc.com.tw/IMINT/'], 
                    ['孩童票/敬老票/愛心票', ChildPrice, 'https://irs.thsrc.com.tw/IMINT/'], 
                    #['11人以上團體票', GroupPrice, 'https://grp.thsrc.com.tw/tkcs_b2c/home/list?cp2Token=NAHF-0JF2-IL9D-EPGU-5YJJ-YYB7-F17X-EWQ1']
                    ]
        
        # 高鐵票價查詢若勾選全部優惠，有些沒有優惠的車次就不會跳出，造成Google Map 傳來的車次(沒有優惠)找不到，這些沒有優惠的車次在後台數據裡，data['data']['DepartureTable']['TrainItem']['Discount']為空，自然也找不到'早鳥','大學生','25人優惠'等字眼，若在最後直接跳出一個ColledgePrice，會跳出UndefinedError，所以要先檢查TrainDiscount是否為空
        # 大學生優惠是單獨的一類，其他優惠都是放在全票或團體票中，就算沒有優惠字典也不會是空的，但若沒有大學生優惠，會印出一個空的字典，因此要特別檢查: len(ColledgePrice) == 0?
        if len(TrainDiscount.keys()) != 0 and len(ColledgePrice) != 0:            
            Result.append([ColledgePrice[0], ColledgePrice[1], 'https://irs.thsrc.com.tw/IMINT/'])

        return Result

    # print(HSHR('高鐵台中站','新左營站','2020/01/01','12:17','821'))

    def Railway(start, end, train_number):
        driver = webdriver.Chrome(executable_path ='C:\\Users\\linda\\Downloads\\chromedriver_win32\\chromedriver.exe')
        driver.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")
        #前往台鐵車次與票價搜尋頁面
        startpoint = driver.find_element_by_name("startStation")
        startpoint.send_keys(start)

        endpoint = driver.find_element_by_name("endStation")
        endpoint.send_keys(end)

        confirm_button = driver.find_element_by_name("query")
        confirm_button.click()
        
        html = driver.page_source

        
        soup = BeautifulSoup(html, 'html.parser')

        '''找車次'''
        attr = {"title":"列車時刻表(另開新視窗)"}
        train_number_list = []
        train_number_tags = soup.find_all("a", attrs = attr)
        for tag in train_number_tags:
            train_number_list.append(tag.get_text())

        '''找票價'''
        price_tags =soup.find_all("td")

        i = 0
        price_list = []
        for tag in price_tags:
            t = tag.get_text().strip()
            index_dollar = t.find("$")
            if index_dollar >= 0:
                price_str = t[index_dollar:]
                price_list.append(int(price_str[2:]))

        adult_price_list = []
        kid_price_list = []
        for i in range(len(price_list)):
            if i % 2 == 0:
                adult_price_list.append(price_list[i])
            if i % 2 == 1:
                kid_price_list.append(price_list[i])
        driver.close()
        all_price_list = list(zip(adult_price_list, kid_price_list))
        
        '''建立車次對票價的字典'''
        number2price = dict(zip(train_number_list, all_price_list))
        
        url = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'
        #台鐵車票是在取票時才決訂票的種類，付款時再指定票種即可，故網址相同
        adult = ['全票', number2price[train_number][0], url]
        kid = ['半票', number2price[train_number][1], url]
        #group = ['20人至40人的團體票',int(number2price[train_number][0] * 0.8), url]
        #團體網路訂票系統開放申購時間為每日 09:00~16:30。每日 08:50 可進入填寫資料
        #50人以上需要事先申請
        return adult, kid


api_output_list = GoogleAPI.get_transport_info('台北', '高雄', 2019, 12, 26, 11, 30)
api_output_list = api_output_list[:4]
print(api_output_list)


route_info = []
for leg in api_output_list:
    leg_info = []
    for step in leg:
        if step[0] == 'BUS' and len(step[1]) == 4:
            num_route = step[1]
            full_ticket_price = step[8][1:].split('.')
            full_ticket_price = full_ticket_price[0]
            bus_info = ['客運', GetTicketPrice.Bus(num_route, full_ticket_price)]
            leg_info.append(bus_info)
            #print(step)
        elif step[0] == 'HEAVY_RAIL':
            if step[1] == '高鐵':
                StartStation = step[3]
                EndStation = step[4]
                DepartureDate = step[5]
                DepartureTime = step[6]
                TrainNumber = step[2]
                hsr_info = ['高鐵', GetTicketPrice.HSHR(StartStation, EndStation, DepartureDate, DepartureTime, TrainNumber)]
                leg_info.append(hsr_info)
            else:
                start = step[3]
                end = step[4]
                train_type = step[1]
                if ord(train_type[-1:]) == 34399:
                    train_type = train_type[:-1]
                elif train_type == '復興/區間':
                    train_type = '區間'
                train_number = train_type + step[2]
                # print(start, end, train_number)
                # rail_info = ['台鐵', GetTicketPrice.Railway(start, end, train_number)]
                # leg_info.append(rail_info)
    route_info.append(leg_info)

print(route_info)
