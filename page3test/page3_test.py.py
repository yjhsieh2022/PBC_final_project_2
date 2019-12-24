from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('price_display'))

    return render_template('test_p1.html')

@app.route('/price_display', methods = ['GET', 'POST'])
def price_display():
    return render_template('page3.html')

if __name__ == '__main__':
    app.debug = True
    app.run()