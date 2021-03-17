from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)

db = client['MachineLearningVacancy']

ml = db.ml


result = ml.find({'$or': [{'min payment': {'$gt': 100000}}, {'min payment': {'$gt': 800}}, {'currency': 'USD'}]})
for user in result:
    pprint(user)