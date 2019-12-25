import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


'''建立站名和車站代碼的字典'''
url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip111/view"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

attr = {"class":"traincode_code1"}
train_code_list = []
train_code_tags = soup.find_all("div", attrs = attr)
for tag in train_code_tags:
    train_code_list.append(tag.get_text())

attr = {"class":"traincode_name1"}
train_name_list = []
train_name_without_station = []
train_name_tags = soup.find_all("div", attrs = attr)

for tag in train_name_tags:
    StationName = tag.get_text()
    train_name_list.append(StationName + "車站")
    train_name_without_station.append(StationName)

NameCode = []
for i in range(len(train_code_list)):
    NameCode.append(train_code_list[i] + '-' + train_name_without_station[i])
    
Name2NameCode = {}
for i in range(len(train_code_list)):
    Name2NameCode[train_name_list[i]] = NameCode[i]
'''input起訖點和車次'''
start = input()
if '台' in start:
    startstop = start.replace('台','臺')
end = input()
if '台' in start:
    end = end.replace('台','臺')
start = Name2NameCode[startstop]
end = Name2NameCode[end]
train_number = input()

driver = webdriver.Chrome(executable_path ='C:\\Users\\User\\Desktop\\course in NTU\\選修\\商管程式設計\\chromedriver.exe')
driver.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")
#前往台鐵車次與票價搜尋頁面



def train_price(start, end, train_number):
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
    
'''根據車次尋找對應的票價資訊'''
event = train_price(start, end, train_number)
print(event)

    
'''在訂票網址輸入訂票資訊
driver = webdriver.Chrome(executable_path ='C:\\Users\\User\\Desktop\\course in NTU\\選修\\商管程式設計\\chromedriver.exe')
driver.get("https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query")
startpoint = driver.find_element_by_name("ticketOrderParamList[0].startStation")
startpoint.send_keys(start)
endpoint = driver.find_element_by_name("ticketOrderParamList[0].endStation")
endpoint.send_keys(end)
ridedate = driver.find_element_by_name("ticketOrderParamList[0].rideDate")
ridedate.clear()
ridedate.send_keys(date)
train = driver.find_element_by_name("ticketOrderParamList[0].trainNoList[0]")
train_only_num = filter(str.isdigit, train_number)
train.send_keys(''.join(list(train_only_num)))
#輸入車次時不加車種才符合搜尋格式'''