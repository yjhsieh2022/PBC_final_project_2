"""
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

# 計算最低總價，用於第二頁顯示"XX元起"
def lowest(pricelist):
    lowestsum = []            
    for routeprice in pricelist:
        lowest = 0
        for price in routeprice:
            if type(price) is dict:
                minprice = min(price.values())
            elif price == '市內公車票價依各縣市不同':
                minprice = 0
            else:
                minprice = price
            lowest += minprice
        lowest = '$'+str(lowest)+'起'
        lowestsum.append(lowest)
    return lowestsum
"""
def create_p2_template(routes_num, API_Result, ticket_num, Price, ticket, pricelist_result, pricesum_result):
# 中間變數先填好
    # 儲存中間的html碼
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_21.html', mode='r', encoding='utf-8') as html_21:
        html_21_Lines = html_21.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_22.html', mode='r', encoding='utf-8') as html_22:
        html_22_Lines = html_22.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_23.html', mode='r', encoding='utf-8') as html_23:
        html_23_Lines = html_23.readlines()
    # 寫進中間的template
    Change_22_Lines = html_22_Lines
    Change_23_Lines = html_23_Lines
    for route_num in range(routes_num):
        r_trans_num = len(API_Result[route_num])
        if route_num == 0:  # 如果是重新來過，要覆寫
            with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_2.html', mode='w', encoding='utf-8') as html_2:
                html_2.writelines(html_21_Lines)
        else:
            with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_2.html', mode='a', encoding='utf-8') as html_2:
                html_2.writelines(html_21_Lines)
        for tran_num in range(r_trans_num):  # 幾種交通工具複製幾次
            with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_2.html', mode='a', encoding='utf-8') as html_2:
                if API_Result[route_num][tran_num][0] == 'BUS': # BUS的API輸出順序跟其他車種不一樣，對應位置要變
                    for line in Change_22_Lines:
                        line = line.replace("startstation", str(API_Result[route_num][tran_num][2]))
                        line = line.replace("endstation", str(API_Result[route_num][tran_num][3]))
                        line = line.replace("starttime", str(API_Result[route_num][tran_num][5]))
                        line = line.replace("transtype", "客運"+str(API_Result[route_num][tran_num][1].strip('L')))
                        line = line.replace("endtime", str(API_Result[route_num][tran_num][7]))
                        line = line.replace("transprice", str(pricelist_result[route_num][tran_num]))
                        html_2.write(line)
                else:
                    for line in Change_22_Lines:
                        line = line.replace("startstation", str(API_Result[route_num][tran_num][3]))
                        line = line.replace("endstation", str(API_Result[route_num][tran_num][4]))
                        line = line.replace("starttime", str(API_Result[route_num][tran_num][6]))
                        line = line.replace("transtype", str(API_Result[route_num][tran_num][1] + API_Result[route_num][tran_num][2]))
                        line = line.replace("endtime", str(API_Result[route_num][tran_num][8]))
                        line = line.replace("transprice", str(pricelist_result[route_num][tran_num]))
                        html_2.write(line)
        with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_2.html', mode='a', encoding='utf-8') as html_2:
            for line in Change_23_Lines:
                line = line.replace("pricetype", str(ticket))
                line = line.replace("pricesum", str(pricesum_result[route_num]))
                html_2.write(line)

    # 儲存html碼
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_1.html', mode='r', encoding='utf-8') as begin:
        Begin_Lines = begin.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_2.html', mode='r', encoding='utf-8') as middle:
        Middle_Lines = middle.readlines()
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2_3.html', mode='r', encoding='utf-8') as end:
        End_Lines = end.readlines()

    # 寫進template
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2.html', mode='w', encoding='utf-8') as combination:
        combination.writelines(Begin_Lines)
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2.html', mode='a', encoding='utf-8') as combination:
        combination.writelines(Middle_Lines)
    with open(file='C:\\Users\\Hsiao Wan-Ju\\Desktop\\TaiwanGo\\templates\\web_page2.html', mode='a', encoding='utf-8') as combination:
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

routes_num = len(API_Result)
ticket_num = 1  # 半票

create_p2_template(routes_num, API_Result, ticket_num)
"""