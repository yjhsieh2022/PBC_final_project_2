from selenium import webdriver
from bs4 import BeautifulSoup

#在台鐵官網填寫起訖點，獲取車次與票價資訊
driver = webdriver.Chrome(executable_path ='C:\\Users\\User\\Desktop\\course in NTU\\選修\\商管程式設計\\chromedriver.exe')
driver.get("https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")

startpoint = driver.find_element_by_name("startStation")
startpoint.send_keys("1000-臺北")
'''以臺北站為例'''

endpoint = driver.find_element_by_name("endStation")
endpoint.send_keys("4400-高雄")
'''以高雄站為例'''

confirm_button = driver.find_element_by_name("query")
confirm_button.click()
'''按確認(注意未選時間)'''

html = driver.page_source
driver.close()

#爬車次與票價資訊

soup = BeautifulSoup(html, 'html.parser')

'''找車次'''
attr = {"title":"列車時刻表(另開新視窗)"}
train_number_list = []
train_number_tags = soup.find_all("a", attrs = attr)
for tag in train_number_tags:
    train_number_list.append(tag.get_text())
print(train_number_list)

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
        
print(adult_price_list)
print(kid_price_list)
