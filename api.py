# 1ое задание

import requests
from pprint import pprint
import json

username = 'Sorbus220'

main_link = 'https://api.github.com/users/'+username+'/repos'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.408', 'Agent': '*/*'}

response = requests.get(main_link, headers=headers)

j_body = response.json()

pprint(j_body)
with open('Repos.json', 'w', encoding="utf-8") as write_js:
   json.dump(j_body, write_js)

pprint(j_body)

# 2ое задание

import requests
from pprint import pprint
import json
user = 'Sorbus'
tag = 'Kekw'

main_link = 'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'+user+'/'+tag+''

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.408', 'Agent': '*/*', "X-Riot-Token": "RGAPI-aa0953c6-fbb2-457a-8716-1fdc30a350ea"}

response = requests.get(main_link, headers=headers)

j_body = response.json()

with open('Riot.json', 'w', encoding="utf-8") as write_js:
   json.dump(j_body, write_js)

pprint(j_body)