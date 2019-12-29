from flask import Flask, request, render_template, redirect, url_for
from combination import GoogleAPI
from combination import GetTicketPrice

taiwango = Flask(__name__)

@taiwango.route('/', methods=['GET', 'POST'])  # 佳妤，taiwango 首頁
def home():
    if request.method == 'POST':
        return redirect(url_for('routechoices', startpoint = request.form.get('startpoint'), destination = request.form.get('destination'), date = request.form.get('date'), startTime = request.form.get('startTime'), ticket = request.form.get('ticket')))
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
    if routes_num == 0:
        return render_template('web_page2_one.html', API_Result = API_Result, Price = Price, routes_num = routes_num)
    # r1_trans_num = count(API_Result[0])
    # r2_trans_num = count(API_Result[1])
    # r3_trans_num = count(API_Result[2])
    # r4_trans_num = count(API_Result[3])

    '''routes_num = 1  # 之後合併要改成連結API的結果
    r1_trans_num = 1
    r2_trans_num = 1
    r3_trans_num = 1
    r4_trans_num = 1

    if routes_num == 0:
        if request.method == 'POST':
            return redirect(url_for('home'))
        return render_template('web_page2_none.html')

    elif routes_num == 1:
        if request.method == 'POST':
            return redirect(url_for('pricechoices'))  # 補足丟進def的參數
        return render_template('web_page2_one.html')

    elif routes_num == 2:
        return render_template('web_page2_two.html')
    elif routes_num == 3:
        return render_template('web_page2_three.html')
    elif routes_num == 4:
        return render_template('web_page2_four.html')'''



@taiwango.route('/pricechoices')  # 宜蓁，選擇之單一路線詳細價格資訊
def pricechoices():  # 輸入需要的參數
    # 在這裡呼叫各交通工具的def
    return 'here is the price!'


if __name__ == '__main__':
    taiwango.debug = True
    taiwango.run()