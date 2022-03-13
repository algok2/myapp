#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests
import myKeys


# In[18]:


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

access_key = myKeys.access_key
secret_key = myKeys.secret_key
server_url = myKeys.server_url

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key).decode('utf8')
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}
res = requests.get(server_url + "/v1/accounts", headers=headers)
wallet = res.json()

for i in range(len(wallet)):
    if wallet[i].get('currency') != 'KRW':
        balance_locked = float(wallet[i].get('balance'))+float(wallet[i].get('locked'))
        print('KRW-'+wallet[i].get('currency') +' '+ '{}'.format(balance_locked) +' '+ wallet[i].get('avg_buy_price'))

