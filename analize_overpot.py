#%%
import numpy as np
import pandas as pd

#%%
PATH = r'PokerAnalysis\Reports\SRP_BTNvsBB_CB_All_All\report_mod.csv'

#%%
df = pd.read_csv(PATH)
columns = df.columns
df.head()

#%%
df[df['overpot']==True].to_csv(r'PokerAnalysis\Reports\SRP_BTNvsBB_CB_All_All\BTNvsBB_over-pot-CB.csv')

#%%
