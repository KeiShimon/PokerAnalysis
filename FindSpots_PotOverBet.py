#%%
import numpy as np
import pandas as pd

#%%
PATH = r'PokerAnalysis\Reports\SRP_BTNvsBB_CB_All_All\report_mod.csv'

#%%

#%%
df = pd.read_csv(PATH)
columns = df.columns

#%%
print('len:', len(df))
print('size:', df.size)

df.head()

#%%
'''Run this block to insert a column that tells if the flop involves overpot-bet strategy.

Definition of overpot situations:
    - absolute overpot frequency < 10%
    - relative overpot frequency occupation among available bet sizes > 20%
'''

THRESHOLD_ABS = 10
THRESHOLD_RELATIVE = 20
OVERBET = 'Bet75.0'

b, f = [], []

for overpot, bet in df.loc[:,[OVERBET, 'Bet']].itertuples(index=False):
    relative = 100 * overpot / bet
    f.append(relative)

    if overpot >= THRESHOLD_ABS and relative >= THRESHOLD_RELATIVE:
        b.append(True)
    else:
        b.append(False)

df['overpot'] = b
df['overpot_freq'] = f

del b, f

df.head()

#%%
df.to_csv(PATH,index=None)
