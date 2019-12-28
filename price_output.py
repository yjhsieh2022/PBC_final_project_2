# coding=utf8
'''
Price = [[['台鐵', (['全票', 23, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 12, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])],['高鐵', [['全票', {'標準車廂': 1350, '商務車廂': 2230, '自由座': 1305}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 675, '商務車廂': 1115, '自由座': 650}, 'https://irs.thsrc.com.tw/IMINT/']]],['台鐵', (['全票', 25, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 13, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 23, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 12, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])],['高鐵', [['全票', {'標準車廂': 1490, '商務車廂': 2440, '自由座': 1445}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 745, '商務車廂': 1220, '自由座': 720}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 67, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 34, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 1530, '商務車廂': 2500, '自由座': 1480}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 765, '商務車廂': 1250, '自由座': 740}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 67, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 34, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
         [['台鐵', (['全票', 752, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 376, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]

Price = [[['客運', [['全票', 50], ['半票', 25]]]],
		 [['台鐵', (['全票', 81, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 41, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['客運', [['全票', 95], ['半票', 48]]]],
		 [['客運', [['全票', 85], ['半票', 43]]]]]
'''
Price = [[['客運', None],['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['客運', None], ['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]
       

# page1 傳來的票種選擇: 暫定參數為tickettype = '全票', '優惠票' 
tickettype = '全票'

# 將各條路線的價格擷取出來，放入pricelist
def pricelist(tickettype, Price):
    pricelist = []
    if tickettype == '全票':
        for routes in Price:
            RoutePrice = []
            for vehicle in routes:
                if vehicle[1] != None:
                    RoutePrice.append(vehicle[1][0][1])
                else:
                    RoutePrice.append('市內公車票價依各縣市不同')
            pricelist.append(RoutePrice)
    if tickettype == '優惠票':
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
                link.append('客運尚無線上訂票系統')
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
            lowest += minprice
        lowest = '$'+str(lowest)+'起'
        lowestsum.append(lowest)
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

print(pricelist('全票', [[['客運', None],['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['客運', None], ['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]
    ))
    
print(hyperlink([[['客運', None],['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['客運', None], ['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]
    ))

print(lowest(pricelist('全票', [[['客運', None],['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['客運', None], ['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]
    )))

print(pricesum(pricelist('全票', [[['客運', None],['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 308, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 154, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['客運', None], ['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 32, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 16, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 670, '商務車廂': 1210, '自由座': 645, '早鳥65折': 435, '早鳥8折': 535, '早鳥9折': 600, '大學生75折': 500}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 335, '商務車廂': 605, '自由座': 320}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]
    )))
