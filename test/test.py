from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('test_p1.html')

@app.route('/go', methods=['GET', 'POST'])
def go():
    #  利用request取得使用者端傳來的方法為何
    if request.method == 'POST':
                          #  利用request取得表單欄位值
        return 'From' + request.values['startpoint'] + 'To' + request.values['destination']
    
    #  非POST的時候就會回傳一個空白的模板
    return render_template('test_p2.html')

if __name__ == '__main__':
    app.debug = True
    app.run()