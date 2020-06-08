from flask import Flask, render_template,request
import locale
from store_parser_by_link import get_store_randevu,get_html

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    locale.setlocale(locale.LC_ALL, "ru_RU")
    try:
        link = request.form['link']
        print(link)
        info=get_store_randevu(link)
        print(info)
    except:
        info = None
    return render_template('index.html', info=info)


@app.route('/store')
def store():
    locale.setlocale(locale.LC_ALL, "ru_RU")
    return render_template('store_page.html')


@app.route('/admin')
def admin_panel():
    locale.setlocale(locale.LC_ALL, "ru_RU")
    return render_template('admin_panel.html')


if __name__ == '__main__':
    app.run(debug=True)
