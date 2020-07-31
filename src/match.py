# Issue Area Codes
# Matching clean df_cb ands scrape output
# Nick Zeppos
# Summer 2020

# imports
import re
import pandas as pd
from pprint import pprint
import numpy as np
import os

# Read congressional bills data
df_cb = pd.read_csv('./data/bills_93_114_clean.csv', sep=',',
                    header=0, encoding='ISO-8859-1')

# insert empty column to populate
df_cb['PolicyArea'] = np.nan

# Get a list of all the file names with congress.gov data
file_names = [file for file in os.listdir("./data/cong_gov_dat")]

# Loopin and matchin
for file in file_names:

    # Construct path
    path = './data/cong_gov_dat/' + file

    pprint(path)

    # Read data
    dat = pd.read_csv(path)

    # Clean up data-- remove punctuation, push to lower
    dat['bill_type'] = dat['bill_type'].str.replace('[^\w\s]', '')
    dat['bill_type'] = dat['bill_type'].str.lower()

    # remove non digits from congress, convert to int
    dat['congress'] = dat['congress'].str.replace(r'\D+', '')
    dat['congress'] = dat['congress'].astype(int)

    pprint(df_cb['PolicyArea'].value_counts())
    na_count = df_cb['PolicyArea'].isna().sum()
    pprint('na count: ' + str(na_count))

    for i, r in dat.iterrows():

        bt = r['bill_type']
        bn = r['bill_number']
        c = r['congress']
        pa = r['policy_area']

        df_cb.loc[(df_cb['BillType'] == bt) & (df_cb['BillNum'] == bn)
                  & (df_cb['Cong'] == c), 'PolicyArea'] = pa

    pprint(df_cb['PolicyArea'].value_counts())
    na_count = df_cb.isna().sum()
    pprint('na count: ' + str(na_count))

df_cb.to_csv('./data/merged.csv', index=False)
