# Issue Area Codes
# Backfilling CB data
# Nick Zeppos
# Summer 2020

# Imports
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from pprint import pprint
import numpy as np
import math
import time
from num2words import num2words

# Read in data
dat = pd.read_csv('./data/merged_edited.csv')
for i, r in dat.iterrows():
    print(i)
    if i % 10000 == 0:
        print('writing to csv...')
        dat.to_csv("./data/merged_edited.csv", index=False)
        remain_uncoded = dat['PolicyArea'].value_counts()
        remain_uncoded = remain_uncoded['uncoded']
        pprint(str(remain_uncoded) + ' remain as uncoded values...')
        time.sleep(1)

    if pd.isnull(r['PolicyArea']):

        base_url = 'https://www.congress.gov/bill/'
        c = num2words(r['Cong'], to='ordinal_num')

        if r['BillType'] == 'hr':
            b = 'house-bill/'
        else:
            b = 'senate-bill/'

        bn = str(r['BillNum'])
        url = base_url + c + '-congress/' + b + bn + '/subjects'
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Check if its a reserved bill
        if 'Reserved Bill' in soup.find('h1').text:
            print('reserved bill...')
            dat.loc[i, 'PolicyArea'] = 'uncoded'
            continue
        else:

            node = soup.find('div', class_='column-aside')
            node = node.find('ul', class_='plain')

            if node is not None:
                pa = node.find('li').text
                dat.loc[i, 'PolicyArea'] = pa
            else:
                dat.loc[i, 'PolicyArea'] = 'uncoded'
