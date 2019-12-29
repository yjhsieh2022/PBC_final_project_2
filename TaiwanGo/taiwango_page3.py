"""
# page1 傳來的票種選擇: 暫定參數為ticket = 0(全票), 1(半票) 

# 將各條路線的價格擷取出來，放入pricelist
def pricelist(ticket, Price):
    pricelist = []
    if ticket == 0:
        for routes in Price:
            RoutePrice = []
            for vehicle in routes:
                if vehicle[1] != None:
                    RoutePrice.append(vehicle[1][0][1])
                else:
                    RoutePrice.append('市內公車票價依各縣市不同')
            pricelist.append(RoutePrice)
    if ticket == 1:
        for routes in Price:
            RoutePrice = []
            for vehicle in routes:
                if vehicle[1] != None:
                    RoutePrice.append(vehicle[1][1][1])
                else:
                    RoutePrice.append('市內公車票價依各縣市不同')
            pricelist.append(RoutePrice) 
    return pricelist
    
def hyperlink(Price):
    hyperlink = []
    for route in Price:
        link = []
        for vehicle in route:
            if vehicle[0] == '客運':
                link.append('尚無線上訂票系統')
            elif vehicle[0] == '台鐵':
                link.append('https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query')
            elif vehicle[0] == '高鐵':
                link.append('https://irs.thsrc.com.tw/IMINT/')
        hyperlink.append(link)
    return hyperlink

def pricesum(pricelist): 
    cal_price = []
    for routeprice in pricelist:
        otherlist = []
        HSHRlist = []
        for vehicle_price in routeprice:
            if type(vehicle_price) is int:
                otherlist.append(vehicle_price)
            if type(vehicle_price) is dict:
                HSHRlist = list(vehicle_price.values())
        temp = [HSHRlist, otherlist]
        cal_price.append(temp)
        
    sum = []
    for route in cal_price:
        routesum = 0
        if route[0] == []:
            for otherprice in route[1]:
                routesum += otherprice
            sum.append(routesum)
        if route[0] != []:
            HSHR = []
            for HSHRprice in route[0]:
                for otherprice in route[1]:
                    HSHRprice += otherprice
                HSHR.append(HSHRprice)
            sum.append(HSHR)
    return sum
"""

def create_p3_template(routes_num, r_trans_num, API_Result, Price, ticket_num):
# 中間變數先填好
    # 儲存中間的html碼
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_21.html', mode='r', encoding='utf-8') as html_21:
        html_21_Lines = html_21.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_221.html', mode='r', encoding='utf-8') as html_221:
        html_221_Lines = html_221.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_222.html', mode='r', encoding='utf-8') as html_222:
        html_222_Lines = html_222.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_23.html', mode='r', encoding='utf-8') as html_23:
        html_23_Lines = html_23.readlines()
    # 寫進中間的template
    Change_221_Lines = html_221_Lines
    Change_222_Lines = html_222_Lines
    Change_23_Lines = html_23_Lines
    
    # 不像第二頁除route_num=0時要複寫其餘不斷疊加，第三頁只有一條路線，不論route_num等於多少都要重寫
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_2.html', mode='w', encoding='utf-8') as html_2:
        html_2.writelines(html_21_Lines)
    for tran_num in range(r_trans_num):  # 幾種交通工具複製幾次
        with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_2.html', mode='a', encoding='utf-8') as html_2:
            if Price[route_num][tran_num][1] != None: 
                if API_Result[route_num][tran_num][0] == 'BUS': # BUS的API輸出順序跟其他車種不一樣，對應位置要變
                    for line in Change_221_Lines:
                        line = line.replace("startstation", str(API_Result[route_num][tran_num][2]))
                        line = line.replace("endstation", str(API_Result[route_num][tran_num][3]))
                        line = line.replace("starttime", str(API_Result[route_num][tran_num][5]))
                        line = line.replace("transtype", str(API_Result[route_num][tran_num][0] + ' ' + API_Result[route_num][tran_num][1]))
                        line = line.replace("endtime",str(API_Result[route_num][tran_num][7]))
                        line = line.replace("price", str(pricelist(ticket_num, Price)[route_num][tran_num]))
                        line = line.replace("hyperlink", str(hyperlink(Price)[route_num][tran_num]))
                        html_2.write(line)
                else:
                    for line in Change_221_Lines:
                        line = line.replace("startstation", str(API_Result[route_num][tran_num][3]))
                        line = line.replace("endstation", str(API_Result[route_num][tran_num][4]))
                        line = line.replace("starttime", str(API_Result[route_num][tran_num][6]))
                        line = line.replace("transtype", str(API_Result[route_num][tran_num][1] + ' ' + API_Result[route_num][tran_num][2]))
                        line = line.replace("endtime",str(API_Result[route_num][tran_num][8]))
                        line = line.replace("price", str(pricelist(ticket_num, Price)[route_num][tran_num]))
                        line = line.replace("hyperlink", str(hyperlink(Price)[route_num][tran_num]))
                        html_2.write(line)
            else: # 沒有票價(不能做按紐)的市內公車用沒有按鈕的p3_test222, API輸出順序跟其他車種不一樣，對應位置要變
                for line in Change_222_Lines:
                    line = line.replace("startstation", str(API_Result[route_num][tran_num][2]))
                    line = line.replace("endstation", str(API_Result[route_num][tran_num][3]))
                    line = line.replace("starttime", str(API_Result[route_num][tran_num][5]))
                    line = line.replace("transtype", str(API_Result[route_num][tran_num][0] + ' ' + API_Result[route_num][tran_num][1]))
                    line = line.replace("endtime",str(API_Result[route_num][tran_num][7]))
                    line = line.replace("price", str(pricelist(ticket_num, Price)[route_num][tran_num]))
                    line = line.replace("hyperlink", str(hyperlink(Price)[route_num][tran_num]))
                    html_2.write(line)
    with open(file='C:\\Users\\宜蓁\\Documents\\大五\\python\\final_project\\WJtest\\templates\\web_page3_2.html', mode='a', encoding='utf-8') as html_2:
        for line in Change_23_Lines:
            line = line.replace("pricetype", str(Price[route_num][tran_num][1][ticket_num][0]))
            line = line.replace("pricesum", str(pricesum(pricelist(ticket_num, Price))[route_num]))
            html_2.write(line)

    # 儲存html碼
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_1.html', mode='r', encoding='utf-8') as begin:
        Begin_Lines = begin.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_2.html', mode='r', encoding='utf-8') as middle:
        Middle_Lines = middle.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3_3.html', mode='r', encoding='utf-8') as end:
        End_Lines = end.readlines()

    # 寫進template
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3.html', mode='w', encoding='utf-8') as combination:
        combination.writelines(Begin_Lines)
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3.html', mode='a', encoding='utf-8') as combination:
        combination.writelines(Middle_Lines)
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page3.html', mode='a', encoding='utf-8') as combination:
        combination.writelines(End_Lines)
    return None

"""
API_Result = [[['BUS', 'L112', '桃園市政府', '桃園火車站', '2020/01/02', '上午11:17', '2020/01/02', '上午11:25', '$15.00'], ['HEAVY_RAIL', '自強號', '121', '桃園車站', '臺中車站', '2020/01/02', '上午11:30', '2020/01/02', '下午1:13']],
              [['HEAVY_RAIL', ' 自強號', '121', '桃園車站', '臺中車站', '2020/01/02', '上午11:30', '2020/01/02', '下午1:13']],
              [['BUS', 'L112', '桃園市政府', '桃園火車站', '2020/01/02', '上午11:33', '2020/01/02', '上午11:41', '$15.00'], ['HEAVY_RAIL', '復興/區間', '1172', '桃園車站', '板橋車站', '2020/01/02', '上午11:46', '2020/01/02', '下午12:12'], ['HEAVY_RAIL', '高鐵', '825', '板橋車站', '高鐵台中站', '2020/01/02', '下午12:19', '2020/01/02', '下午1:15'], ['HEAVY_RAIL', '復興/區間', '2194', '新烏日火車站', '臺中車站', '2020/01/02', '下午1:25', '2020/01/02', '下午1:37']],
              [['HEAVY_RAIL', '復興/區間', '1172', '桃園車站', ' 板橋車站', '2020/01/02', '上午11:46', '2020/01/02', '下午12:12'], ['HEAVY_RAIL', '高鐵', '825', '板橋車站', '高鐵台中站', '2020/01/02', '下午12:19', '2020/01/02', '下午1:15'], ['HEAVY_RAIL', '復興/區間', '2194', '新烏日火車站', '臺中車站', '2020/01/02', '下午1:25', '2020/01/02', '下午1:37']]]
Price = [[['客運', None], ['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
         [['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
         [['客運', None], ['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, ' 商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
         [['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心 票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]

route_num = 0
r_trans_num = len(API_Result[route_num])
ticket_num = 0  # 全票

create_p3_template(route_num, r_trans_num, API_Result, Price, ticket_num)
"""