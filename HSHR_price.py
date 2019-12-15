import requests
import json

#setting
StartStationName = '南港站'
EndStationName = '左營站'
DepartureSearchDate = '2019/12/27'
DepartueSearchTime = '18:30'
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
           '左營站':'f2519629-5973-4d08-913b-479cce78a356'
}

# 高鐵車次號碼首位為1或0，若首位為0，google map會自動省略僅顯示三位數，需手動加零高鐵票價查詢系統爬價格才會對
TrainNumber = '693'#675
if len(TrainNumber) == 3:
    NewTrainNumber = '0' + TrainNumber
if len(TrainNumber) == 4:
    NewTrainNumber = TrainNumber
    
    
# 因為高鐵採用call api獲取json資料的方式，使用requests/selenium都無法在html網頁上直接抓到價格。XHR/Request URL取得真的存有價格的網址，透過requests.post(api)的方式來獲取資料

url = "http://www.thsrc.com.tw/tw/TimeTable/Search"
form_data = {
    'StartStation': Station[StartStationName],
    'StartStationName': StartStationName,
    'EndStation': Station[EndStationName],
    'EndStationName': EndStationName,
    'DepartueSearchDate': DepartureSearchDate,
    'DepartueSearchTime': DepartueSearchTime,
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
            

earlybird = {'65折起':['65折','8折','9折'], '8折起':['8折','9折']}
if '早鳥' in TrainDiscount.keys():
    if TrainDiscount['早鳥'] == ['65折起']:
        TrainDiscount['早鳥'] = earlybird['65折起']
    elif TrainDiscount['早鳥'] == ['8折起']:
        TrainDiscount['早鳥'] = earlybird['8折起']
if '校外教學' in TrainDiscount.keys():
    if TrainDiscount['校外教學'] == ['4/7折']:
        TrainDiscount['校外教學'] = ['4折', '7折']

header = ['全票', '孩童票/敬老票/愛心票', '團體票']
Coach = data['data']['PriceTable']['Coach']
Business = data['data']['PriceTable']['Business']
Unreserved = data['data']['PriceTable']['Unreserved']
for keys in TrainDiscount.keys():
    for values in TrainDiscount[keys]:
        for Column in data['data']['PriceTable']['Column']:
            if Column['ColumnName'] == values:
                header.append(keys+Column['ColumnName'])
                Coach.append(Column['CoachPrice'])

for i in range(len(header)):
    if header[i] == '校外教學4折':
        header[i] = '小學生校外教學4折'
    if header[i] == '校外教學7折':
        header[i] = '中學、大學生校外教學7折'
   
print(header)
print(Coach)
print(Business)
print(Unreserved)

import pandas as pd
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
price= [Coach, Business, Unreserved]
df = pd.DataFrame(price, index = ['普通車廂', '商務車廂', '自由座車廂'], columns = header)
df = df.fillna(" ")
# 設置顯示列/行數，不然行列數太多會自動省略變成...
# 顯示所有列
pd.set_option('display.max_columns',None)
# 顯示所有行
pd.set_option('display.max_rows', None)
# 設定寬度無限
pd.set_option('display.width', None)
print(df)
 

