#%%
import pandas as pd
import numpy as np

from decimal import Decimal, ROUND_HALF_UP
from pandas import DataFrame, Series

#%%
'''Set defaul parameters below and run this block.
'''

PATH = r'PokerAnalysis\Reports\SRP_BTNvsBB_CB_All_All\report_IP_Full.csv'
INITIALPOT = 50

#%%
'''Run this block to initialize a DataFrame.
'''
df = pd.read_csv(PATH)
print('Loaded Dataframe from:', PATH)
print('     size:', df.size)
print('     length:', len(df))
df.head(10)

#%%
'''Run this block to delete unnecessary columns and change names.
'''

change_column_name = {}
deleted_columns = []

for c in df.columns:
    colname = c.lower()
    colname = colname.replace(' ', '_')

    if 'ev' in colname:
        deleted_columns.append(c)
        del df[c]

    else:
        if 'bet' in colname or 'raise' in colname:
            i = colname.find('%')
            betsize = str(int(colname[4:i]) * 100 / INITIALPOT)
            action = 'raise' if ( 'raise' in colname ) else 'bet'
            colname = action + betsize

        elif 'check' in colname:
            colname = 'check'

        change_column_name[c] = colname


df = df.rename(columns=change_column_name)

print('Column names have been changed as below:')
for k in change_column_name:
    print('  ', k, '->', change_column_name[k])

print('\nThese columns have been deleted:')
for k in deleted_columns:
    print('  ', k)

del change_column_name, deleted_columns, action, betsize, colname, k, c

print('\n')
print('--------------df.head()--------------')
df.head()

#%%
'''Run this block to insert columns.

Columns inserted:
    tone, pair, btm, mid, top (in this order)
    bet (before check)

Columns are inserted right next to 'flop'.

'''
flops = df['flop']
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

insert_col = df.columns.get_loc('weight_ip') + 1

df.insert(insert_col,'tone',tone)
df.insert(insert_col,'pair',pair)
df.insert(insert_col,'btm',btm)
df.insert(insert_col,'mid',mid)
df.insert(insert_col,'top',top)

del tone, pair, btm, mid, top, flops, flop, t, m, b

df.insert(df.columns.get_loc('check'), 'bet', [100-x for x in df['check']])

print('Columns inserted: top, mid, btm, pair, tone, bet')

print('\n')
print('--------------df.head()--------------')
df.head()

#%%
'''Run this cell to add a row that tells if the board involves over-pot-CB strategy.
TRUE/FALSE will be copied from board-wise report.
'''
PATH_board_wise_report = r'PokerAnalysis\Reports\SRP_BTNvsBB_CB_All_All\report_mod.csv'

df_board_wise = pd.read_csv(PATH_board_wise_report)
df_board_wise.head()

i = 0
current_flop = df_board_wise.loc[i]['flop']
last_flop = current_flop
flags = []
flag = df_board_wise.loc[i]['potover']

for current_flop in df['flop']:

    if current_flop == last_flop:
        flags.append(flag)

    else:
        i += 1
        flag = df_board_wise.loc[i]['potover']
        flags.append(flag)

    last_flop = current_flop

df['potover_board'] = flags
del flags, flag, df_board_wise, current_flop, last_flop
print('Columns concatenated: "potover_board"')

print('\n')
print('--------------df.head()--------------')
df.head()

#%%
'''Run this cell to concatenate columns that tells if the specific hand involves over-pot-CB strategy.
Check default parameters before run.
'''

THRESHOLD_ABS = 10
THRESHOLD_RELATIVE = 20
POTOVER = 'bet150.0'

b, f = [], []

for potover, bet in df.loc[:,[POTOVER, 'bet']].itertuples(index=False):
    relative = 100 * float(Decimal(str(potover / bet)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
    f.append(relative)

    if potover >= THRESHOLD_ABS and relative >= THRESHOLD_RELATIVE:
        b.append(True)
    else:
        b.append(False)

df['potover_hand'] = b
df['potover_freq'] = f

del b, f, potover, bet

print('Columns concatenated: "potover_hand", "potover_freq"')

print('\n')
print('--------------df.head()--------------')
df.head()

#%%
df.to_csv(PATH, index=None)

#%%
df.head()

#%%
'''Run this cell to concatenate:

    straight
    flush
    set
    twopair


    flush_draw
    straight_draw_eight
    straight_draw_four
    backdoor_flush_draw
    backdoor_open_end

'''