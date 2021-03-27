import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

mail_url = 'https://news.mail.ru'
mail_response = requests.get(mail_url, headers=header)
mail_dom = html.fromstring(mail_response.text)
mail_news = mail_dom.xpath('//div[@class="js-module"]//a/@href')

ya_url = 'https://yandex.ru/news/'
ya_response = requests.get(ya_url, headers=header)
ya_dom = html.fromstring(ya_response.text)
ya_news = ya_dom.xpath('//div[contains(@class, "news-top-flexible-stories")]/div[contains(@class, "mg-grid__col")]')

lenta_url = 'https://lenta.ru/'
lenta_response = requests.get(lenta_url, headers=header)
lenta_dom = html.fromstring(lenta_response.text)
lenta_news = lenta_dom.xpath('//section[contains(@class, "b-top7-for-main")]//div[contains(@class, "item")]')

news_list = []

for link in mail_news:
    news_dict = link
    news_list.append(news_dict)


final_list = []
for url in news_list:
    response_news = requests.get(url, headers=header)
    dom2 = html.fromstring(response_news.text)
    container = dom2.xpath('//div[contains(@class,"article ")]')

    for news in container:
        fil_dict = {}
        name = news.xpath('.//span[@class="hdr__text"]/h1[@class="hdr__inner"]/text()')
        date = news.xpath('.//div[contains(@class,"breadcrumbs")]//span[@class="note"]//@datetime')
        source = news.xpath('//div[contains(@class,"breadcrumbs")]//span[@class="link__text"]/text()')
        fil_dict['url'] = url
        fil_dict['name'] = name
        fil_dict['date'] = date
        fil_dict['source'] = source

        final_list.append(fil_dict)
        break

for ynews in ya_news:
    y_dict = {}
    name = ynews.xpath('.//h2[@class="mg-card__title"]/text()')
    name = name[0].replace(u'\xa0', u' ')
    date = ynews.xpath('.//span[@class="mg-card-source__time"]/text()')
    source = ynews.xpath('.//a[@class="mg-card__source-link"]/text()')
    link = ynews.xpath('.//@href')

    y_dict['name'] = name
    y_dict['date'] = date
    y_dict['source'] = source
    y_dict['url'] = link[0]
    final_list.append(y_dict)

for lnews in lenta_news:
    l_dict = {}
    name = lnews.xpath('.//a[@href]/text()')
    name = name[0].replace(u'\xa0', u' ')
    date = lnews.xpath('.//@datetime')
    link = lnews.xpath('.//@href')

    l_dict['name'] = name
    l_dict['date'] = date
    l_dict['source'] = ['Lenta.ru']
    l_dict['url'] = lenta_url + link[0]
    final_list.append(l_dict)
pprint(final_list)

client = MongoClient('localhost', 27017)

db = client['News']

newsdb = db.newsdb

newsdb.insert_many(final_list)
