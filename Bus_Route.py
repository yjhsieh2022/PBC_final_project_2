import requests
from selenium import webdriver
from bs4 import BeautifulSoup

def get_bus_price(num_route, full_ticket_price, ticket_type):
    '''
    num_route = input(路線編號:)
    data_pickedroute = '0_,' + str(num_route) + '_,0'
    full_ticket_price = input(全票價格:)
    ticket_type = input(全票輸入1,半票輸入0:)
    '''
    data_pickedroute = '0_,' + str(num_route) + '_,0'
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
        
    if ticket_type == 1:
        return full_ticket_price
    else:
        return Full2Half[full_ticket_price]

print(get_bus_price('1062', '61', '0'))
