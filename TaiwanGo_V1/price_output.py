# coding=utf8

# 將各條路線的價格擷取出來，放入pricelist
def pricelist(ticket_num, Price):
    pricelist = []
    if ticket_num == 0:
        for routes in Price:
            RoutePrice = []
            for vehicle in routes:
                if vehicle[1] != None:
                    if vehicle[1][0] == '全票':
                        RoutePrice.append(vehicle[1][1])
                    else:
                        RoutePrice.append(vehicle[1][0][1])
                else:
                    RoutePrice.append('市內公車票價依各縣市不同')
            pricelist.append(RoutePrice)
    if ticket_num == 1:
        for routes in Price:
            RoutePrice = []
            for vehicle in routes:
                if vehicle[1] != None:
                    if vehicle[1][1] == '半票':
                        RoutePrice.append(vehicle[1][1])
                    else:
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
            lowest += int(minprice)
        lowest_str = '$'+str(lowest)+'起'
        lowestsum.append(lowest_str)
    return lowestsum

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
ticket_num = 0
Price = [[['台鐵', (['全票', 40, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 20, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
         [['台鐵', (['全票', 49, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 25, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
         [['客運', ['全票', 98]]],
         [['客運', [['全票', 85], ['半票', 43]]]]]
# Price = [[['台鐵', (['全票', 20, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 10, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 1460, '商務車廂': 2390, '自由座': 1415}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 730, '商務車廂': 1195, '自由座': 705}, 'https://irs.thsrc.com.tw/IMINT/']]]], [['台鐵', (['全票', 20, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 10, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車 廂': 1460, '商務車廂': 2390, '自由座': 1415}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 730, '商務車廂': 1195, '自由座': 705}, 'https://irs.thsrc.com.tw/IMINT/']]]]] 
price_result = pricelist(ticket_num, Price)
print(price_result)
print(lowest(price_result))
"""