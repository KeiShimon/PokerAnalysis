#%%
import numpy as np
import pandas as pd
import sys
from pandas import Series, DataFrame

#%%
'''
Set defaul parameters below and run this block.
'''
PATH = r"Reports\SRP_BTNvsBB_CB_All_All\report.csv"
INITIALPOT = 100 # default is 100

#%%
'''
Run this block to initialize a DataFrame.
'''
df = pd.read_csv(PATH,header=3)
print('loaded Dataframe, size: ', df.size)
df.head(10)

#%%
'''
Run this block to delete unnecessary columns and change names.
'''

change_column_name = {'Global %':'Occurence'}
deleted_columns = []

for colname in df.columns:

    if 'EV' in colname:
        deleted_columns.append(colname)
        del df[colname]

    elif 'BET' in colname or 'RAISE' in colname:
        i = colname.find('%')
        betsize = str(int(colname[4:i]) * 100 / INITIALPOT)
        action = 'Bet' if 'BET' in colname else 'Raise'
        change_column_name[colname] = action + betsize

    elif 'CHECK' in colname:
        change_column_name[colname] = 'Check'

    elif 'Global' not in colname:
        change_column_name[colname] = colname.replace(' ', '_').replace('Equity','EQ')

    elif 'Global' in colname:
        change_column_name[colname] = 'global'

df = df.rename(columns=change_column_name)

print('The names of these columns have been changed using dictionary below:')
for k in change_column_name:
    print('  ', k, ':', change_column_name[k])

print('\nThese columns have been deleted:')
for k in deleted_columns:
    print('  ', k)

del change_column_name, deleted_columns, action, betsize, colname, k

print('\n')
print('--------------df.head()--------------')
df.head()


#%%
'''
Run this cell to insert columns.

Columns inserted:
    tone, pair, btm, mid, top (in this order)

Columns are inserted right next to Global.

'''
flops = Series(df['Flop'])
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
                tone.append(2)
            else:
                tone.append(1)
        elif t == b or m == b:
            tone.append(2)
        else:
            tone.append(3)

    else:
        top.append(0)
        mid.append(0)
        btm.append(0)
        pair.append(0)
        tone.append(0)


df.insert(2,'tone',tone)
df.insert(2,'pair',pair)
df.insert(2,'btm',btm)
df.insert(2,'mid',mid)
df.insert(2,'top',top)

del tone, pair, btm, mid, top, flops, flop, t, m, b

print('Columns inserted: top, mid, btm, pair, tone')

print('\n')
print('--------------df.head()--------------')
df.head()

#%%
'''
Run this cell to save current DataFrame
'''
new_path = PATH[0:PATH.find('.csv')] + '_mod.csv'
df.to_csv(new_path, index=None)

print('Saved df to', new_path)

#%%


#%%
