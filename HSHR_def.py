"""
#setting
StartStation = '高鐵台中站'
EndStation = '新左營站'
DepartureDate = '2020/01/01'
DepartureTime = '下午12:17'
TrainNumber = '821'
"""

def HSHR(StartStation, EndStation, DepartureDate, DepartureTime, TrainNumber):
    
    import requests
    import json
    
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
    
    FullPrice = {'標準車廂':int(Coach[0][1:]),'商務車廂':int(Business[0][1:]),'自由座':int(Unreserved[0][1:])}
    ChildPrice = {'標準車廂':int(Coach[1][1:]),'商務車廂':int(Business[1][1:]),'自由座':int(Unreserved[1][1:])}

 
    """團體票先註解掉
    GroupPrice = {'標準車廂':int(Coach[2][1:]),'商務車廂':int(Business[2][1:])}  
    ColledgePrice = []
    """
    
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
                    FullPrice['早鳥'+Column['ColumnName']] = int(Column['CoachPrice'][1:])                    
    if '大學生' in TrainDiscount.keys():
        for values in TrainDiscount['大學生']: 
            for Column in data['data']['PriceTable']['Column']:
                if Column['ColumnName'] == values:
                    FullPrice['大學生'+Column['ColumnName']] = int(Column['CoachPrice'][1:])
    """
    if '25人團體' in TrainDiscount.keys():            
        for values in TrainDiscount['25人團體']: 
            for Column in data['data']['PriceTable']['Column']:
                if Column['ColumnName'] == values:
                    GroupPrice['25人團體'+Column['ColumnName']] = int(Column['CoachPrice'][1:])
    if '校外教學' in TrainDiscount.keys():
        for values in TrainDiscount['校外教學']:
            for Column in data['data']['PriceTable']['Column']:
                if Column['ColumnName'] == values:
                    if values == '4折':
                        GroupPrice['小學生校外教學4折'] = int(Column['CoachPrice'][1:])
                    elif values == '7折':
                        GroupPrice['中學、大學生校外教學7折'] = int(Column['CoachPrice'][1:])
    """
    Result = [  ['全票',FullPrice, 'https://irs.thsrc.com.tw/IMINT/'], 
                ['孩童票/敬老票/愛心票', ChildPrice, 'https://irs.thsrc.com.tw/IMINT/'], 
                #['11人以上團體票', GroupPrice, 'https://grp.thsrc.com.tw/tkcs_b2c/home/list?cp2Token=NAHF-0JF2-IL9D-EPGU-5YJJ-YYB7-F17X-EWQ1']
                ]
    """
    # 高鐵票價查詢若勾選全部優惠，有些沒有優惠的車次就不會跳出，造成Google Map 傳來的車次(沒有優惠)找不到，這些沒有優惠的車次在後台數據裡，data['data']['DepartureTable']['TrainItem']['Discount']為空，自然也找不到'早鳥','大學生','25人優惠'等字眼，若在最後直接跳出一個ColledgePrice，會跳出UndefinedError，所以要先檢查TrainDiscount是否為空
    # 大學生優惠是單獨的一類，其他優惠都是放在全票或團體票中，就算沒有優惠字典也不會是空的，但若沒有大學生優惠，會印出一個空的字典，因此要特別檢查: len(ColledgePrice) == 0?
    if len(TrainDiscount.keys()) != 0 and len(ColledgePrice) != 0:            
        Result.append([ColledgePrice[0], ColledgePrice[1], 'https://irs.thsrc.com.tw/IMINT/'])
    """
    return Result

print(HSHR('高鐵台中站','新左營站','2020/01/01','下午12:17','821'))
