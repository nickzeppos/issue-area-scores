# Issue area codes
# Investigating data

# Imports
import numpy as np
import pandas as pd
from pprint import pprint

# Read in dat
dat = pd.read_csv('./code_scheme_comparison_93_114.csv')

# Group by Major
# dat_major = dat.groupby(['Major', 'PolicyArea']).size().to_csv(
#     'major_policyarea_grouped.csv')

dat_uncoded = dat[dat['PolicyArea'] == 'uncoded']
dat_uncoded_grp = dat_uncoded.groupby(['Cong']).size()
print(dat_uncoded_grp)
