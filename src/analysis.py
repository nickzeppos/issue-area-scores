# Issue area codes
# Investigating data

# Imports
import numpy as np
import pandas as pd
from pprint import pprint
import os

# Read in dat
dat = pd.read_csv('./dat/code_scheme_comparison_93_114.csv')

# Uncoded bills slicing and dicing
# Table uncoded by congress, chamber
uncoded = dat[dat['PolicyArea'] == 'uncoded']
uncoded_congress_chamber = uncoded.groupby(
    ['Cong', 'BillType']).size().to_frame()

# Table uncoded by congress, chamber, for all major categories
uncoded_congress_chamber_policyArea = uncoded.groupby(
    ['Cong', 'BillType', 'Major']).size().to_frame()

# Write to file
# uncoded_ch_co_pa.to_csv('./dat/uncoded_by_cong_chamb_major.csv')

# Deprecated codes slicing and dicing
# Table 93rd by chamber, for all policy areas, to demonstrate some of the deprecated codes
ninetyThirdCongress = dat[dat['Cong'] == 93]
ninetyThirdCongress_policyArea = ninetyThirdCongress.groupby(
    ['Cong', 'BillType', 'PolicyArea']).size().to_frame()

# Write to file
# ninetyThirdCongress_policyArea.to_csv('./dat/93rd_policyAreas.csv')

# Unique codes in the 93rd
ninetyThirdCongress_policyArea_noChamberSplit = ninetyThirdCongress.groupby(
    ['PolicyArea']).size().to_frame()

# Write to file
# ninetyThirdCongress_policyArea_noChamberSplit.to_csv(
#    './dat/93rd_policyAreas_noChamberSplit.csv')

# Total unique codes
# print(dat.groupby('PolicyArea').size().to_frame())

# Total unique codes per congress
print(dat.groupby('Cong')['PolicyArea'].nunique())

# Investigate child welfare
childWelfare_congress = dat[dat['PolicyArea'] == 'Child welfare']
childWelfare_congress_major = childWelfare_congress.groupby(
    ['Cong', 'Major']).size().to_frame()
# print(childWelfare_congress_major)

# Investigate credit cards
creditCards_congress = dat[dat['PolicyArea'] == 'Credit cards']
creditCards_congress_major = creditCards_congress.groupby(
    ['Cong', 'Major']).size().to_frame()
print(creditCards_congress_major)

# Investigate vietnamese conflict
vietnameseConflit_congress = dat[dat['PolicyArea'] == 'Vietnamese Conflict']
vietnameseConflict_congress_major = vietnameseConflit_congress.groupby(
    ['Cong', 'Major']).size().to_frame()
print(vietnameseConflict_congress_major)
