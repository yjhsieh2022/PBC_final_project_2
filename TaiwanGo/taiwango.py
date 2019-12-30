from flask import Flask, request, render_template, redirect, url_for
from api_combined import GoogleAPI, GetTicketPrice
from price_output import pricelist, hyperlink, lowest, pricesum
from taiwango_page2 import create_p2_template
# from taiwango_page3 import create_p3_template

taiwango = Flask(__name__)

@taiwango.route('/', methods=['GET', 'POST'])  # 佳妤，taiwango 首頁
def home():
    if request.method == 'POST':
        return redirect(url_for('routechoices', startpoint=request.form.get('startpoint'), destination=request.form.get('destination'), date=request.form.get('date'), startTime=request.form.get('startTime'), ticket=request.form.get('ticket')))
    return render_template('web_page1.html')

@taiwango.route('/routechoices/<startpoint>/<destination>/<date>/<startTime>/<ticket>', methods=['GET', 'POST'])  # 婉如，各路線選擇
def routechoices(startpoint, destination, date, startTime, ticket):
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    hour = int(startTime[:2])
    minutes = int(startTime[3:])
    
    API_Result = GoogleAPI.get_transport_info(startpoint, destination, year, month, day, hour, minutes)
    Price = GetTicketPrice.total_price_list(API_Result)
    routes_num = len(API_Result)

    if ticket == '全票':
        ticket_num = 0
    elif ticket == '半票':
        ticket_num = 1

    if routes_num == 0:
        if request.method == 'POST':
            return redirect(url_for('home'))
        return render_template('web_page2_none.html')

    elif routes_num == 1:
        if request.method == 'POST':
            return redirect(url_for('pricechoices'))  # 補足丟進def的參數
        create_p2_template(routes_num, API_Result, ticket_num, Price, ticket)
        return render_template('web_page2.html')

    elif routes_num == 2:
        if request.method == 'POST':
            return redirect(url_for('pricechoices'))  # 補足丟進def的參數
        create_p2_template(routes_num, API_Result, ticket_num, Price, ticket)
        return render_template('web_page2.html')

    elif routes_num == 3:
        if request.method == 'POST':
            return redirect(url_for('pricechoices'))  # 補足丟進def的參數
        create_p2_template(routes_num, API_Result, ticket_num, Price, ticket)
        return render_template('web_page2.html')

    elif routes_num == 4:
        if request.method == 'POST':
            return redirect(url_for('pricechoices'))  # 補足丟進def的參數
        create_p2_template(routes_num, API_Result, ticket_num, Price, ticket)
        return render_template('web_page2.html')


@taiwango.route('/pricechoices')  # 宜蓁，選擇之單一路線詳細價格資訊
def pricechoices():  # 輸入需要的參數
    # 在這裡呼叫各交通工具的def
    return 'here is the price!'


if __name__ == '__main__':
    taiwango.debug = True
    taiwango.run()