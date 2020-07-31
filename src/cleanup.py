# Issue Area Codes
# Cleaning up CB data
# Nick Zeppos
# Summer 2020

# Imports
import re
import pandas as pd
from pprint import pprint

# Read in data
df_cb = pd.read_csv('./data/bills93-114.csv', sep=';',
                    header=0, encoding='ISO-8859-1')
df = pd.read_csv("./data/out.csv")

## Cleaning up ##

# Cleaning df_cb
# Get only hr and s BillType from df_cb, store as df_cb_bills
df_cb_bills = df_cb[df_cb['BillType'].isin(['hr', 's'])]

# Take columns BillNum, BillType, Cong, and Major
df_cb_bills = df_cb_bills[['BillNum', 'BillType', 'Cong', 'Major']]

# Drop rows where Major == 99, which refers to private bills
df_cb_bills = df_cb_bills[df_cb_bills['Major'] != 99.0]

# Convert Major codes from numbers to corresponding text values
# Values can be found here: https://www.comparativeagendas.net/pages/master-codebook
df_cb_bills.loc[df_cb_bills['Major'] == 1.0, 'Major'] = 'macroeconomics'
df_cb_bills.loc[df_cb_bills['Major'] == 2.0, 'Major'] = 'civil rights'
df_cb_bills.loc[df_cb_bills['Major'] == 3.0, 'Major'] = 'health'
df_cb_bills.loc[df_cb_bills['Major'] == 4.0, 'Major'] = 'agriculture'
df_cb_bills.loc[df_cb_bills['Major'] == 5.0, 'Major'] = 'labor'
df_cb_bills.loc[df_cb_bills['Major'] == 6.0, 'Major'] = 'education'
df_cb_bills.loc[df_cb_bills['Major'] == 7.0, 'Major'] = 'environment'
df_cb_bills.loc[df_cb_bills['Major'] == 8.0, 'Major'] = 'energy'
df_cb_bills.loc[df_cb_bills['Major'] == 9.0, 'Major'] = 'immigration'
df_cb_bills.loc[df_cb_bills['Major'] == 10.0, 'Major'] = 'transportation'
df_cb_bills.loc[df_cb_bills['Major'] == 12.0, 'Major'] = 'law and crime'
df_cb_bills.loc[df_cb_bills['Major'] == 13.0, 'Major'] = 'social welfare'
df_cb_bills.loc[df_cb_bills['Major'] == 14.0, 'Major'] = 'housing'
df_cb_bills.loc[df_cb_bills['Major'] == 15.0, 'Major'] = 'domestic commerce'
df_cb_bills.loc[df_cb_bills['Major'] == 16.0, 'Major'] = 'defense'
df_cb_bills.loc[df_cb_bills['Major'] == 17.0, 'Major'] = 'technology'
df_cb_bills.loc[df_cb_bills['Major'] == 18.0, 'Major'] = 'foreign trade'
df_cb_bills.loc[df_cb_bills['Major'] ==
                19.0, 'Major'] = 'international affairs'
df_cb_bills.loc[df_cb_bills['Major'] ==
                20.0, 'Major'] = 'government operations'
df_cb_bills.loc[df_cb_bills['Major'] == 21.0, 'Major'] = 'public lands'
df_cb_bills.loc[df_cb_bills['Major'] == 23.0, 'Major'] = 'culture'

# Write df_cb_bills to csv
df_cb_bills.to_csv('./data/bills_93_114_clean.csv', index=False)
