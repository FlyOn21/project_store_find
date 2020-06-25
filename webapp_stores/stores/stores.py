from webapp_stores import standard_icon, db_functions
from bs4 import BeautifulSoup
from webapp_stores import get_query




# Butik

def get_butik_data(url='https://www.butik.ru'):
    html = get_query.get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string
        name = 'Butik.ru'
        link = soup.find('link', rel="icon", type="image/png")
        icon = url + (link['href'])
        online = True
        url = url
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)
    else:
        online = False
        url = url
        name = 'Butik.ru'
        title = 'Магазин временно недоступен'
        icon = standard_icon.standard_icon()
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)


# Randevu

def get_randevu_data(url='https://www.rendez-vous.ru'):
    html = get_query.get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string
        name = 'Rendezvous'
        icon = soup.find('meta', property="og:image", )['content']
        online = True
        url = url
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)

    else:
        online = False
        url = url
        name = 'Rendezvous'
        title = 'Магазин временно недоступен'
        icon = standard_icon.standard_icon()
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)


# Aliexpress

def get_ali_data(url = 'https://aliexpress.ru/'):
    html = get_query.get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string
        name = 'Aliexpress'
        icon = soup.find('meta', property="og:image")['content']
        online = True
        url = url
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)
    else:
        online = False
        url = url
        name = 'Aliexpress'
        title = 'Магазин временно недоступен'
        icon = standard_icon.standard_icon()
        db_functions.save_data(title=title, online=online, url=url,
                               name=name, icon=icon)
