from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient
from pymongo import UpdateOne



main_link = 'https://www.hh.ru'

target = 'Java'
sub = 'д'
sub2 = 'т'
salary = 150000 # в рублях
salaryUSD = salary/74
salaryEUR = salary/88
params = {'L_is_autosearch': 'false', 'clusters': 'true', 'enable_snippets': 'true', 'schedule': 'remote',
          'text': target, 'page': '0'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}

response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
bad_chars = ['\xa0']
vacancys = []
i = True
pagenumber = 0


def spliternormal(a):
    pay = a.split(' ')
    pay_amount = pay[0].split('-')
    currency = pay[1]
    min_pay = int(pay_amount[0])
    max_pay = int(pay_amount[1])
    return currency, min_pay, max_pay, pay_amount


def spliternot(a):
    pay = a.split(' ')
    prefix = pay[0]
    pay_amount = int(pay[1])
    currency = pay[2]
    return prefix, pay_amount, currency


while True:
    params = {'clusters': 'true', 'area': '1', 'L_is_autosearch': 'false', 'enable_snippets': 'true', 'text': target,
              'page': pagenumber}
    response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
    if response.ok:
        soup = bs(response.text, 'html.parser')
        vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item'})
        try:
            target = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}).getText()
        except Exception as e:
            target = "последняя страница"
        if target == "дальше":
            for vacancy in vacancy_list:
                vacancy_data = {}
                vacancy_name = vacancy.find('a').getText()
                try:
                    vacancy_pay = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
                    vacancy_pay = "".join(r for r in vacancy_pay if r not in bad_chars)
                    if sub in vacancy_pay:
                        vacancy_data['max payment'] = spliternot(vacancy_pay)[1]
                        vacancy_data['currency'] = spliternot(vacancy_pay)[2]
                    if sub2 in vacancy_pay:
                        vacancy_data['min payment'] = spliternot(vacancy_pay)[1]
                        vacancy_data['currency'] = spliternot(vacancy_pay)[2]
                    else:
                        vacancy_data['min payment'] = spliternormal(vacancy_pay)[1]
                        vacancy_data['max payment'] = spliternormal(vacancy_pay)[2]
                        vacancy_data['currency'] = spliternormal(vacancy_pay)[0]
                except Exception as e:
                    vacancy_pay = None
                vacancy_link = vacancy.find('a')['href']
                vacancy_data['name'] = vacancy_name
                vacancy_data['link'] = vacancy_link
                vacancy_data['website'] = main_link
                vacancys.append(vacancy_data)
            pagenumber = pagenumber + 1
        else:
            for vacancy in vacancy_list:
                vacancy_data = {}
                vacancy_name = vacancy.find('a').getText()
                try:
                    vacancy_pay = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
                    vacancy_pay = "".join(r for r in vacancy_pay if r not in bad_chars)
                    if sub in vacancy_pay:
                        vacancy_data['max payment'] = spliternot(vacancy_pay)[1]
                        vacancy_data['currency'] = spliternot(vacancy_pay)[2]
                    if sub2 in vacancy_pay:
                        vacancy_data['min payment'] = spliternot(vacancy_pay)[1]
                        vacancy_data['currency'] = spliternot(vacancy_pay)[2]
                    else:
                        vacancy_data['min payment'] = spliternormal(vacancy_pay)[1]
                        vacancy_data['max payment'] = spliternormal(vacancy_pay)[2]
                        vacancy_data['currency'] = spliternormal(vacancy_pay)[0]
                except Exception as e:
                    vacancy_pay = None
            break
pprint(vacancys)
pprint(len(vacancys))

client = MongoClient('localhost', 27017)

db = client['MachineLearningVacancyNew']

ml = db.ml

upserts = [UpdateOne({'name': x['name']}, {'$setOnInsert': x}, upsert=True) for x in vacancys]

ml.bulk_write(upserts)

result = ml.find({'$or': [{'$and': [{'min payment': {'$gt': salary}}, {'currency': 'руб.'}]},
                          {'$and':[{'min payment': {'$gt': salaryUSD}}, {'currency': 'USD'}]},
                          {'$and': [{'min payment': {'$gt': salaryEUR}}, {'currency': 'EUR'}]},
                          {'$and': [{'max payment': {'$gt': salary}}, {'currency': 'руб.'}]},
                          {'$and': [{'max payment': {'$gt': salaryUSD}}, {'currency': 'USD'}]},
                          {'$and': [{'max payment': {'$gt': salaryEUR}}, {'currency': 'EUR'}]}]})
