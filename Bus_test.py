from selenium import webdriver
from bs4 import BeautifulSoup

driver_taiwanbus = webdriver.Chrome(executable_path ='C:\\Users\\linda\\Downloads\\chromedriver_win32\\chromedriver.exe')
driver_taiwanbus.get('https://www.taiwanbus.tw/ByLine.aspx?Lang=')

# 1首頁，輸入路線編號(之後要做成Def)
input_taiwanbus = driver_taiwanbus.find_element_by_xpath('//input[@value="-請輸入路線編號-"]')
input_taiwanbus.send_keys('1088')
searching_button = driver_taiwanbus.find_element_by_xpath('//img[@src="images/btn_08.png"]')
searching_button.click()
driver_taiwanbus.current_url
searching_ways = driver_taiwanbus.find_element_by_xpath('//div[@id="SelectData"]/table/tbody/tr/td/a')
searching_ways.click()

# 2進入該路線動線頁面
