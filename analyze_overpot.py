#%%
import numpy as np
import pandas as pd

#%%
PATH = r'PokerAnalysis\Reports\SRP_BTNvsBB_CB_All_All\BTNvsBB_over-pot-CB.csv'
PATH_legacy = r'PokerAnalysis\Reports\SRP_BTNvsBB_CB_All_All\report_mod.csv'

#%%
df = pd.read_csv(PATH, index_col=0)
columns = df.columns
df.head()

#%%
df = df.sort_values(by=['overpot_freq'], ascending=False)
df

#%%
df.to_csv(PATH)

#%%
