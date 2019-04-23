#%%
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

#%%
filepass, INITIALPOT = '3B.P SB vs BTN PairBoards.csv', 200
df = pd.read_csv(filepass,header=3)
df.head()

#%%

changeColName = {'Global %':'Occurence'}
for colname in df.columns:

    if 'EV' in colname:
        del df[colname]

    elif 'BET' in colname:
        i = colname.find('%')
        betsize = str(int(colname[4:i]) * 100 / INITIALPOT)
        changeColName[colname] = 'Bet' + betsize

    elif 'CHECK' in colname:
        changeColName[colname] = 'Check'
    
    elif 'Global' not in colname:
        changeColName[colname] = colname.replace(' ', '_').replace('EQR','EqR').replace('Equity','Eq')

df = df.rename(columns=changeColName)


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

df.to_csv(filepass,index=None)
df.head()

#%%
