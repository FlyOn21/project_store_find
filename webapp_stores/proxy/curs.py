from webapp_stores.proxy import get_query
from bs4 import BeautifulSoup
import os


def get_curs_usd():
    curs = get_query.get_html_all(url='https://www.banki.ru/products/currency/cb/')
    if curs:
        soup = BeautifulSoup(curs, 'html.parser')
        res = ((((soup.find('tbody')).find('tr')).find_all('td'))[3]).text
        with open('curs_today.txt', 'w', encoding='utf-8') as file:
            file.write(res)
            file.close()



def curs_open():
    with open(os.path.abspath('webapp_stores/proxy/curs_today.txt'), 'r', encoding='utf-8') as file_two:
        curs = file_two.read()
    return float(curs)


if __name__ == "__main__":
    curs_open()
