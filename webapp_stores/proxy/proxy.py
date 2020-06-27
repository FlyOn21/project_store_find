import requests as re
import webapp_stores.config as conf


def proxy():
    try:
        proxy_json = re.get(conf.PROXY_API_URL)
        pr = proxy_json.text
        with open('proxy.txt', 'w', encoding='utf-8') as file:
            file.writelines(str(pr))
            file.close()
    except(re.RequestException,ValueError):
        print('ошибка обновления proxy_list')

if __name__=='__main__':
    proxy()