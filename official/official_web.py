from flask import Flask, request, render_template, redirect, url_for

taiwango = Flask(__name__)

@taiwango.route('/', methods=['GET', 'POST'])  # 佳妤，taiwango 首頁
def home():
    if request.method == 'POST':
        return redirect(url_for('routechoices'))

    return render_template('web_page1.html')

if __name__ == '__main__':
    taiwango.debug = True
    taiwango.run()