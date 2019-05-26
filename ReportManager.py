#%%
import numpy as np
import pandas as pd
import sys
from pandas import Series, DataFrame

#%%
def main(*argv):

    PATH = argv[0]
    try:
        INITIALPOT = int(argv[1])
    except:
        INITIALPOT = 100
    
    df = pd.read_csv(PATH,header=3)

    # change column name
    changeColName = {'Global %':'Occurence'}

    for colname in df.columns:

        if 'EV' in colname:
            del df[colname]

        elif 'BET' in colname or 'RAISE' in colname:
            i = colname.find('%')
            betsize = str(int(colname[4:i]) * 100 / INITIALPOT)
            action = 'Bet' if 'BET' in colname else 'Raise'
            changeColName[colname] = action + betsize

        elif 'CHECK' in colname:
            changeColName[colname] = 'Check'
        
        elif 'Global' not in colname:
            changeColName[colname] = colname.replace(' ', '_').replace('EQR','EqR').replace('Equity','Eq')

    df = df.rename(columns=changeColName)

    # insert columns that describe flop profile
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

    new_path = PATH[0:PATH.find('.csv')] + '_mod.csv'

    df.to_csv(new_path,index=None)

    sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])