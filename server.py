from flask import Flask, render_template
import locale

app = Flask(__name__)


@app.route('/')
def index():
    locale.setlocale(locale.LC_ALL, "ru")
    return render_template('index.html')


@app.route('/store')
def store():
    locale.setlocale(locale.LC_ALL, "ru")
    return render_template('store_page.html')


@app.route('/admin')
def admin_panel():
    locale.setlocale(locale.LC_ALL, "ru")
    return render_template('admin_panel.html')


if __name__ == '__main__':
    app.run(debug=True)
