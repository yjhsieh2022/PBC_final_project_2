import requests
from selenium import webdriver
from bs4 import BeautifulSoup

num_route = input()
data_pickedroute = '0_,' + str(num_route) + '_,0'

'''找到填入url的代號'''
data_topost = {'Type':'GetKey', 'Data':data_pickedroute, 'Lang':'#'}
r_route = requests.post('https://www.taiwanbus.tw/APP_API/Test/ByLine.aspx', data=data_topost, verify=False)
R_Route = [ r.strip('_') for r in r_route.text.split(',')]
# print(R_Route)

'''填入代號連到路線頁面'''
url_route_page = 'https://www.taiwanbus.tw/information.aspx?Lang=Cht&Line=' + str(R_Route[4])  # 這裡是採用去程:R[4]；如果回程:R[9]
# print(url_route_page)
route_page = webdriver.Chrome(executable_path ='C:\\Users\\Hsiao Wan-Ju\\Downloads\\chromedriver.exe')
route_page.get(url_route_page)

'''填入代號連到價格頁面'''
url_price_page = 'https://web.taiwanbus.tw/eBUS/subsystem/ticket/TMSquery.aspx?run_id=' + str(R_Route[4])  # 這裡是採用去程:R[4]；如果回程:R[9]
# print(url_price_page)
price_page = webdriver.Chrome(executable_path ='C:\\Users\\Hsiao Wan-Ju\\Downloads\\chromedriver.exe')
price_page.get(url_price_page)
