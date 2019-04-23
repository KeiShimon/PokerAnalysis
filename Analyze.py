#%%
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import seaborn as sns
sns.set(style='whitegrid')

#%%
PATH = r'C:\Users\simon\OneDrive\Programming\Poker report\3B.P SB vs BTN PairBoards.csv'
df = pd.read_csv(PATH)
df.head()

#%%
df.head()

#%%
df[(df['pair']==140) & (df['btm']== 3)]

#%%
sns.barplot(x='top', y='OOP_Eq', data=df, ci=None)

#%%
sns.barplot(x='top', y='Bet', data=df, ci=None)

#%%
sns.barplot(x='btm',y='OOP_Eq',data=df[df['top']==14], ci=None)

#%%
sns.barplot(x='btm', y='Bet', data=df[df['top']==14], ci=None)



#%%
g = sns.catplot(x='btm', y='Bet57.5', data=df[df['top']==13], hue='tone', kind='bar', ci=None)
g.set_axis_labels('Rank of another card', 'Bet .58x frequency')

#%%
df_khi = df[df['top']==13]

def f(x):
    if x == 130:
        return 'KKx'
    else:
        return 'Kyy'

tmp_arr = [f(x) for x in df_khi['pair']]

df_khi['Kings?'] = tmp_arr
df_khi.head()

#%%
df_khi.head()

#%%
g = sns.catplot(x='btm', y='Bet57.5', data=df_khi, hue='Kings?', kind='bar', ci=None)
g.set_axis_labels('Rank of another card', 'Bet .58x frequency')


#%%
# 33x と 58x のそれぞれのベットサイズについて、横軸をエクイティ、縦軸をコンボ数とするヒストグラムを作成する
# 加えて、それらの