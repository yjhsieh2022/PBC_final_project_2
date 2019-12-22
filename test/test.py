from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('go'))

    return render_template('test_p1.html')

@app.route('/go', methods=['GET', 'POST'])
def go():
    #  利用request取得使用者端傳來的方法為何
    if request.method == 'POST':
        return redirect(url_for('your_route', startpoint=request.form.get('startpoint'), destination=request.form.get('destination')))
    
    #  非POST的時候就會回傳一個空白的模板
    return render_template('test_p2.html')

@app.route('/your_route/<startpoint>/<destination>')
def your_route(startpoint, destination):
    return render_template('test_p3.html', startpoint=startpoint, destination=destination)

if __name__ == '__main__':
    app.debug = True
    app.run()