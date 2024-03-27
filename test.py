import json

import requests

sentence="俄联邦安全会议副主席梅德韦杰夫当地时间22日在社交平台Telegram上发文称，如果查明这起恐怖袭击的组织者与基辅政权有关，应该将其消灭。"
requestData = {"data": [sentence], "modelname": "bert_crf_klg"}
headers = {'content-type': "application/json"}
res_result = requests.post('http://59.73.128.14:5000/relation', data=json.dumps(requestData), headers=headers)
res_json = res_result.json()
print(res_json)