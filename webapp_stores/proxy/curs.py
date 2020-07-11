from webapp_stores.proxy import get_query
from bs4 import BeautifulSoup


def get_curs_usd():
    curs = get_query.get_html_all(url='https://www.banki.ru/products/currency/cb/')
    if curs:
        soup = BeautifulSoup(curs, 'html.parser')
        res = ((((soup.find('tbody')).find('tr')).find_all('td'))[3]).text
        return (float(res))

if __name__ == "__main__":
    get_curs_usd()