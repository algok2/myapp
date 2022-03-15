#!/usr/bin/env python
# coding: utf-8

# In[4]:


from IPython.core.display import display, HTML
display(HTML('<style>.container {width:100%}</style>'))
from IPython.display import clear_output


# In[5]:


import os, time, rich
import jwt
import uuid
import hashlib
from datetime import datetime
from urllib.parse import urlencode

import requests
import myKeys

from upbitpy import Upbitpy


# In[6]:


upbit = Upbitpy()


# In[7]:


# access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
# secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
# server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

access_key = myKeys.access_key
secret_key = myKeys.secret_key
server_url = myKeys.server_url


# In[8]:


def get_dic(dic):
    payload = { 'access_key': access_key, 'nonce': str(uuid.uuid4()) }
    jwt_token = jwt.encode(payload, secret_key).decode('utf8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.get(server_url + "/v1/accounts", headers=headers)
    wallet = res.json()

    for i in range(len(wallet)):
        if wallet[i].get('currency') != 'KRW':
            balance_locked = float(wallet[i].get('balance'))+float(wallet[i].get('locked'))
            dic['KRW-'+wallet[i].get('currency')] = [wallet[i].get('avg_buy_price') , balance_locked ]
    return dic


# In[9]:


def get_star(x):
    s = ''
    for i in range(x%6+1):
        s = s+'★'
    return s


# In[10]:


def do(cnt):
#     buy_dic = { line.split()[0] : [float(line.split()[2]), float(line.split()[1])] for line in open("input.txt") }
    buy_dic = {}
    buy_dic = get_dic(buy_dic)
    
    if len(buy_dic) > 0:
    
        ticker_list = list(buy_dic.keys())

        sum_profit_loss = 0
        tickers = upbit.get_ticker(ticker_list)

        print('=============================================================================================================')
        print('{:^10}\t: {:^14}\t {:^14}\t ({:^14})\t ({:^10})\t [{:^10}]'.format('CODE', 'CURR', 'BUY', 'GAP', 'Coins', 'P/L'))
        print('-------------------------------------------------------------------------------------------------------------')
        for ticker in tickers:
            code = ticker['market']
            curr_price = float(ticker['trade_price'])
            buy_price = float(buy_dic.get(code)[0])
            step_price = curr_price-buy_price
            profit_loss = int(step_price*buy_dic.get(code)[1])
            print('{0:10}\t: {1:14,.2f}\t {2:14,.2f}\t ({3:+14,.2f})\t ({4:+10,.2f})\t [{5:=+10,}]'.format(code, curr_price, buy_price, step_price, buy_dic.get(code)[1], profit_loss))
            sum_profit_loss = int(sum_profit_loss + profit_loss)
        print('-------------------------------------------------------------------------------------------------------------')
        print('                                                                                           SUM : [{:=+10,}]'.format(sum_profit_loss))
        print('=============================================================================================================')
    else:
        print('--------------------------------------------------------------------------')
        print('There are no coins in your wallet.')
        print('--------------------------------------------------------------------------')
#     time.sleep(10)
#     clear_output(wait=True)


# In[20]:


def local():
    buy_dic = { line.split()[0] : [float(line.split()[2]), float(line.split()[1])] for line in open("input.txt") }
    
    if len(buy_dic) > 0:
        ticker_list = list(buy_dic.keys())
        sum_profit_loss = 0
        tickers = upbit.get_ticker(ticker_list)
        print('--------------------------------------------------------------------------')
        for ticker in tickers:
            code = ticker['market']
            curr_price = int(ticker['trade_price'])
            buy_price = int(buy_dic.get(code)[0])
            step_price = curr_price-buy_price
            profit_loss = int(step_price*buy_dic.get(code)[1])
            print('{0:10}\t: {1:14,.2f}\t {2:14,.2f}\t ({3:+14,.2f})]'.format(code, curr_price, buy_price, step_price, buy_dic.get(code)[1], profit_loss))
            sum_profit_loss = int(sum_profit_loss + profit_loss)
#     print('-------------------------------------------------------------------------------------------------------------')


# In[22]:


cnt = 0
while True:
    curr_time = datetime.now().strftime("%H:%M:%S")
    star =  get_star(cnt)
    rich.print('{}  {}'.format(curr_time, star))
    local()
    do(cnt)
    cnt = cnt+1
    time.sleep(10)


# In[26]:


# jupyter nbconvert --to python upbit_cmd_v0.1.ipynb
cmdCommand_01 = 'copy upbit_cmd_v0.1.ipynb upbit_cmd.ipynb'
cmdCommand_02 = 'jupyter nbconvert --to python upbit_cmd.ipynb'
os.system(cmdCommand_01)
os.system(cmdCommand_02)

