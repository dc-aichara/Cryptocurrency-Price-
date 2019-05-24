import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
from user_agent import generate_user_agent

# generate a user agent
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
#headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.63 Safari/537.36'}
# IP rotation
proxies = {'http' : 'http://10.10.0.0:0000',
          'https': 'http://120.10.0.0:0000'}

url = 'https://coinmarketcap.com/currencies/'

dates ='/historical-data/?start=20130428&end=20190524'

cryptos = ['bitcoin','ethereum','ripple', 'eos', 'litecoin', 'bitcoin-cash', 'tether', 'stellar', 'tron', 'binance-coin','cardano','bitcoin-sv',\
            'monero', 'iota','dash', 'maker']  # , 'neo', 'ethereum-classic','nem', 'zcash'  ,'ontology', 'waves', 'tezos', 'vechain', 'usd-coin']



crypto_price =pd.DataFrame()

content = requests.get(url+ cryptos[0] + dates,headers=headers).content
soup = BeautifulSoup(content, 'html.parser')
table = soup.find('table', {'class': 'table'})

data = [[td.text.strip() for td in tr.findChildren('td')]
        for tr in table.findChildren('tr')]
df = pd.DataFrame(data)
df = df.drop(columns =[1,2,3,4,5,6]) # keep date only
df = df.drop([0])
crypto_price['date'] = df[0]

for crypto in cryptos:
    content = requests.get(url+ crypto + dates,headers=headers).content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'table'})

    data = [[td.text.strip() for td in tr.findChildren('td')]
            for tr in table.findChildren('tr')]
    df = pd.DataFrame(data)
    df = df.drop(columns =[0,1,2,3,5,6]) # Keep only closing price
    df = df.drop([0])
    df[4] = df[4].str.replace(',','', regex =True)
    crypto_price[crypto] = df[4]
    if crypto == 'binance-coin':
        sleep(180)

crypto_price['date'] = pd.to_datetime(crypto_price['date'])
crypto_price = crypto_price.fillna(0)
crypto_price.index = crypto_price['date']
crypto_price = crypto_price.sort_index()
crypto_price = crypto_price.drop(['date'],axis=1)
print('Job is done')

