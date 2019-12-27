from flask import Flask, request, render_template, redirect, url_for

taiwango = Flask(__name__)

@taiwango.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        transport_info = [[['HEAVY_RAIL', '自強號', '271', '松山車站', '台北車站', '2020/01/01', '下午12:35', '2020/01/01', '下午12:42'], ['HEAVY_RAIL', '高鐵', '639', '台北車站', '高鐵台南站', '2020/01/01', '下午12:46', '2020/01/01', '下午2:32'], ['HEAVY_RAIL', ' 復興/區間', '3744', '沙崙車站', '台南車站', '2020/01/01', '下午2:47', '2020/01/01', '下午3:10']],
        [['HEAVY_RAIL', '自強號', '271', '松山車站', '台北車站', '2020/01/01', '下午12:35', '2020/01/01', '下午12:42'], ['HEAVY_RAIL', '高鐵', '639', '台北車站', '新左營站', '2020/01/01', '下午12:46', '2020/01/01', '下午2:45'], ['HEAVY_RAIL', '莒光號', '522', '新左營站', '台南車站', '2020/01/01', '下午3:05', '2020/01/01', '下午3:38']],
        [['HEAVY_RAIL', '復興/區間', '4028', '松山車站', ' 南港車站', '2020/01/01', '下午12:17', '2020/01/01', '下午12:20'], ['HEAVY_RAIL', '高鐵', '639', '南港車站', '新左營站', '2020/01/01', '下午12:35', '2020/01/01', '下午2:45'], ['HEAVY_RAIL', '莒光號', '522', '新左營站', '台南車站', '2020/01/01', '下午3:05', '2020/01/01', '下午3:38']],
        [['HEAVY_RAIL', '自強號', '127', '松山車站', '台南車站', '2020/01/01', '下午1:19', '2020/01/01', '下午4:33']]]
        
        Price = [[['台鐵', (['全票', 23, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 12, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])],['高鐵', [['全票', {'標準車廂': 1350, '商務車廂': 2230, '自由座': 1305}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 675, '商務車廂': 1115, '自由座': 650}, 'https://irs.thsrc.com.tw/IMINT/']]],['台鐵', (['全票', 25, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 13, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 23, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 12, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])],['高鐵', [['全票', {'標準車廂': 1490, '商務車廂': 2440, '自由座': 1445}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 745, '商務車廂': 1220, '自由座': 720}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 67, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 34, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
		 [['台鐵', (['全票', 15, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 8, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])], ['高鐵', [['全票', {'標準車廂': 1530, '商務車廂': 2500, '自由座': 1480}, 'https://irs.thsrc.com.tw/IMINT/'], ['孩童票/敬老票/愛心票', {'標準車廂': 765, '商務車廂': 1250, '自由座': 740}, 'https://irs.thsrc.com.tw/IMINT/']]], ['台鐵', (['全票', 67, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 34, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]],
         [['台鐵', (['全票', 752, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'], ['半票', 376, 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query'])]]]
        
        # page1 傳來的票種選擇: 暫定參數為tickettype = '全票', '優惠票' 
        tickettype = '全票'

        # 將各條路線的價格擷取出來，放入pricelist
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

        hyperlink = []
        for route in Price:
            link = []
            for vehicle in route:
                if vehicle[0] == '客運':
                    link.append('客運無線上購票系統')
                elif vehicle[0] == '台鐵':
                    link.append('https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip123/query')
                elif vehicle[0] == '高鐵':
                    link.append('https://irs.thsrc.com.tw/IMINT/')
            hyperlink.append(link)

        # 計算最低總價，用於第二頁顯示"XX元起"
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

        sum = []   
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

        '''假設第二頁輸出的地點參數如下'''
        station = ['松山車站','台北車站','台北車站','高鐵台南站','沙崙車站','台南車站']
        carnumber = ['自強號271','高鐵639','復興/區間3744']
        time = ['下午12:35','下午12:42','下午12:46', '下午2:32', '下午2:47', '下午3:10']

        return redirect(url_for('price_detail'), station = station, carnumber = carnumber, time = time, hyperlink = hyperlink[0], pricelist = pricelist[0], sum = sum[0])

    return render_template('test_p1.html')


@taiwango.route('/price_detail/<station>/<carnumber>/<time>/<hyperlink>/<pricelist>/<sum>')
def price_detail(station, carnumber, time, hyperlink, pricelist, sum):
    if len(carnumber) == 3:
        return render_template('3trans.html', station = station, carnumber = carnumber, time = time, hyperlink = hyperlink, pricelist = pricelist, sum = sum)

if __name__ == '__main__':
    taiwango.debug = True
    taiwango.run()