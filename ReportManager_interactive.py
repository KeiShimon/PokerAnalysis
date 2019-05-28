#%%
import numpy as np
import pandas as pd
import sys
from pandas import Series, DataFrame
from decimal import Decimal

#%%
'''Set defaul parameters below and run this block.
'''
# PATH =
# INITIALPOT =  # default is 100

#%%
'''Run this block to initialize a DataFrame.
'''
df = pd.read_csv(PATH,header=3)
print('loaded Dataframe, size: ', df.size)
df.head(10)

#%%
'''Run this block to delete unnecessary columns and change names.
'''

change_column_name = {}
deleted_columns = []

for c in df.columns:
    colname = c.lower()
    colname.replace(' ', '_')

    if 'ev' in colname:
        deleted_columns.append(colname)
        del df[colname]

    else:
        if 'bet' in colname or 'raise' in colname:
            i = colname.find('%')
            betsize = str(int(colname[4:i]) * 100 / INITIALPOT)
            action = 'bet' if 'bet' in colname else 'raise'
            colname = action + betsize

        elif 'check' in colname:
            colname = 'check'

        elif 'global' in colname:
            colname = 'global'

        change_column_name[c] = colname

df = df.rename(columns=change_column_name)

print('The names of these columns have been changed using dictionary below:')
for k in change_column_name:
    print('  ', k, '->', change_column_name[k])

print('\nThese columns have been deleted:')
for k in deleted_columns:
    print('  ', k)

del change_column_name, deleted_columns, action, betsize, colname, k

print('\n')
print('--------------df.head()--------------')
df.head()


#%%
'''Run this block to insert columns.

Columns inserted:
    tone, pair, btm, mid, top (in this order)
    bet (before check)

Columns are inserted right next to Global.

'''
flops = Series(df['flop'])
rankToInt = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
top,mid,btm = [], [], []
tone,pair = [], []

for flop in flops:

    if len(flop) > 3:

        # rank and pair
        t,m,b = rankToInt[flop[0]], rankToInt[flop[3]], rankToInt[flop[6]]
        top.append(t)
        mid.append(m)
        btm.append(b)

        if t != b:
            if t!= m and m != b:
                pair.append(0)
            else:
                pair.append(10*m)
        else:
            pair.append(100*t)

        # tone
        t, m, b = flop[1::3]

        if t == m:
            if t != b:
                tone.append(2) # twotone
            else:
                tone.append(3) # monotone
        elif t == b or m == b:
            tone.append(2) # twotone
        else:
            tone.append(1) # rainbow

    else: # average row
        top.append(0)
        mid.append(0)
        btm.append(0)
        pair.append(0)
        tone.append(0)

insert_id = df.columns.get_loc('global') + 1

df.insert(insert_id,'tone',tone)
df.insert(insert_id,'pair',pair)
df.insert(insert_id,'btm',btm)
df.insert(insert_id,'mid',mid)
df.insert(insert_id,'top',top)

del tone, pair, btm, mid, top, flops, flop, t, m, b

df.insert(df.columns.get_loc('check'), 'bet', [100-x for x in df['check']])

print('Columns inserted: top, mid, btm, pair, tone, bet')

print('\n')
print('--------------df.head()--------------')
df.head()

#%%
'''Run this block to insert a column that tells if the flop involves overpot-bet strategy.

Definition of overpot situations:
    - absolute overpot frequency < 10%
    - relative overpot frequency occupation among available bet sizes > 20%
'''

THRESHOLD_ABS = 10
THRESHOLD_RELATIVE = 20
OVERBET = 'bet75.0'

b, f = [], []

for overpot, bet in df.loc[:,[OVERBET, 'bet']].itertuples(index=False):
    relative = 100 * float(Decimal(str(overpot / bet)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
    f.append(relative)

    if overpot >= THRESHOLD_ABS and relative >= THRESHOLD_RELATIVE:
        b.append(True)
    else:
        b.append(False)

df['overpot'] = b
df['overpot_freq'] = f

del b, f

print('Columns inserted: overbet, overbet_freq')
print('\n')
print('--------------df.head()--------------')
df.head()

#%%
'''Run this block to save current DataFrame
'''
new_path = PATH[0:PATH.find('.csv')] + '_mod.csv'
df.to_csv(new_path, index=None)

print('Saved df to', new_path)
