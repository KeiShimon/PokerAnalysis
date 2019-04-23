#%%
from copy import deepcopy
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import random
# import seaborn as sns
# sns.set(style='whitegrid')

#%%
def generatePriority(i, L, previousBet=False):
    '''
    Returns a list of ids. \n
    Iterating this list allows us to access to piles as the order of priorities as flollows: \n
    smaller bet/raise > larger bet/raise \n
    moving from bet: bet > check \n
    moving from raise: raise > call \n
    moving from call: raise(smallest) > fold \n
    '''

    allowed_id = set(range(L))
    priority = []
    
    # checked and deciding between bet and check
    if not previousBet:
        for x in range(1,L):
            left, right = i - x, i + x

            # comparing between bets, smaller bet is higher priority
            if right < L-1:
                if right in allowed_id:
                    priority.append(right)
                if left in allowed_id:
                    priority.append(left)
            # comparing between bet and check, bet is higher priority
            else:
                if left in allowed_id:
                    priority.append(left)
                if right in allowed_id:
                    priority.append(right)

    # deciding between raise, call, fold
    else:
        for x in range(1,L):
            left, right = i - x, i + x

            # comparing between raises, smaller raise is higher priority
            if right < L-2:
                if right in allowed_id:
                    priority.append(right)
                if left in allowed_id:
                    priority.append(left)

            # comparing between raise and call, or raise and fold, raise is higher priority
            else:
                if left in allowed_id:
                    priority.append(left)
                if right in allowed_id:
                    priority.append(right)

    return priority

#%%
def calcEMD(source,comp,previousBet=False):
    '''
    Returns the EMD distance between two lists. \n
    The length of two lists must be same otherwise raise error. \n
    The distance beetween piles is the difference of indices of them.
    '''

    npipes = len(source)

    if len(source) != len(comp):
        raise TypeError('The lengths of input lists to compute EMD do not match.')

    source_copy = deepcopy(source)
    emd = 0

    # try to find the EMD by moving piles of the first list to equalify the second list
    for i in range(npipes):

        # move exceeding amout of the current pile to other piles
        pileToMove = source_copy[i] - comp[i]
        if pileToMove > 0:

            # generate list of ids that represent the priority of target piles
            priority = generatePriority(i, npipes, previousBet)
            j = 0

            # move pile to target pipes by the order of priority-list
            while pileToMove > 0 and j < npipes-1:
                targetPile = priority[j]
                capacity = comp[targetPile] - source_copy[targetPile]

                if capacity > 0:
                    if capacity < pileToMove:
                        source_copy[targetPile] = comp[targetPile]
                        source_copy[i] -= capacity
                        emd += abs(i-targetPile) * capacity
                        pileToMove -= capacity

                    else:
                        source_copy[targetPile] += pileToMove
                        source_copy[i] = comp[i]
                        emd += abs(i-targetPile) * pileToMove
                        pileToMove = 0

                j += 1

    return emd

#%%
def getAverage(arr, nclusters, clusters):
    '''Returns a 2d array of each cluster's average \n
    input arr: 2-d np.array \n
    input clusters: 1-d np.array
    '''

    npoints = len(arr)
    nitems = len(arr[0])
    rowtodelete = set()

    if len(clusters) != npoints:
        raise ValueError('Length of items and cluster-list does not match.')

    # initialize centroids as 2-d array
    ave = np.empty((nclusters,nitems))

    for i in range(nclusters):
        if i in clusters:
            ave[i] = np.average(arr[np.where(clusters==i)], axis=0)        
        else:
            rowtodelete.add(i)

    n = nclusters
    if rowtodelete:
        n = n - len(rowtodelete)
        print('[INFO] Number of clusters has become {}'.format(n))
        for i in rowtodelete:
            ave = np.delete(arr, i, axis=0)

    return ave, n

#%%
def findNearestCentroid(point, centroids):
    '''Returns int: the name of nearest centroid to a given point.\n
        input point: array-like, point we are interested.\n
        input centroids: array-like, average(centroid) of each clusters.\n
    '''

    ncentroids = len(centroids)
    nearestCentroid = ncentroids

    minDistance = float('inf')
    emds = np.empty(ncentroids)

    for i in range(ncentroids):
        emd = calcEMD(point,centroids[i])
        emds[i] = emd
        if emd < minDistance:
            minDistance = emd
            nearestCentroid = i
    
    return nearestCentroid

#%%
def clusterize(data,nclusters,nsteps, initCluster=None, initCentroids=None):
    '''Returns a list of cluster indices each row belongs to.
    '''

    print('[INFO] Starting k-means clustering (NCLUSTERS={})'.format(nclusters))

    # number of points to cluster
    npoints = len(data)

    # initialize clusters and centroids
    nclusters_current = nclusters


    if initCentroids is None:
        if initCluster is None:
            clusters = np.random.randint(nclusters, size=npoints)
        else:
            if type(initCluster) == np.ndarray:
                clusters = initCluster
            else:
                clusters = np.array(initCluster)
    else:
        if len(initCentroids) != nclusters:
            print('[WARNING] number of clusters given by variables \"nclusters\" and \"initCentroids\" does not match.')
            print('[INFO] NCLUSTERS is changed to {}'.format(len(initCentroids)))
            nclusters_current = len(initCentroids)

        clusters = np.empty(npoints)
        for i in range(npoints):
            clusters[i] = findNearestCentroid(data[i], initCentroids)


    for step in range(nsteps):
        prev_clusters = clusters.copy()

        # get centroid of each cluster as a dictionary
        centroids, nclusters_current = getAverage(data, nclusters_current, clusters)

        # for each row find nearest centroid and update the variable 'clusters'
        for i in range(npoints):
            clusters[i] = findNearestCentroid(data[i],centroids)

        # check if clustering has completed
        if len(prev_clusters) == len(clusters):
            if (prev_clusters == clusters).all():
                break

    if step < nsteps-1:
        print('[INFO] k-means clustering (NCLUSTERS={}) completed at {}th iteration.'.format(nclusters, step+1))    
    else:
        print('[INFO] k-means clustering (NCLUSTERS={}) did not converge after {}th iteration.'.format(nclusters,nsteps))
    
    return clusters


#%%
import seaborn as sns
sns.set_style('whitegrid')

#%%
def summerizeClusters(df,clusters,nclusters):

    nstrategies = df.shape[-1]
    arr = []
    
    for cluster in range(nclusters):

        target_df = df[clusters==cluster]
        ndatas = len(target_df)

        if ndatas != 0:

            for strategyID in range(nstrategies):
                arr += [[strategyID, sum(target_df.iloc[:, strategyID]) / ndatas, cluster]]

    return DataFrame(arr, columns=['strategy','frequency','cluster'])


#%%
# initialize np.array from dataframe
PATH = r'C:\Users\simon\OneDrive\Programming\Poker report\3B.P SB vs BTN PairBoards.csv'
df = pd.read_csv(PATH)
df_strategy = df[:len(df)-1].iloc[:,list(df.columns).index('IP_EqR')+1:]
arr = np.array(df_strategy)

print('Printing df.head()')
print(df.head())

print('\nPrinting df_strategy.head()')
print(df_strategy.head())

#%%

NCLUSTERS = 7
NSTEPS = 20
initial = [
    [ 0, 80, 10, 10], # cluster 0
    [ 0, 45, 45, 10], # cluster 1 
    [ 0, 10, 80, 10], # cluster 2
    [ 1, 33, 33, 33],
    [ 5, 45, 25, 25], # cluster 3.0 
    [14, 20, 33, 33], # cluster 3.1 & 4
    [ 2,  3, 50, 45]  # cluster 5 
]

initial_2 = [
    [ 2, 48, 48,  2], # cluster 0
    [ 0, 85, 15,  0], # cluster 1 
    [ 0,  5, 94,  1], # cluster 2
    [15, 50, 10, 25], # cluster 3
    [ 0, 40, 30, 30], # cluster 4
    [15, 25, 25, 35], # cluster 5
    [ 0,  0, 55, 45]  # cluster 6 
]

clusters = clusterize(arr,NCLUSTERS,NSTEPS,initCentroids=initial)
df_forplotting = summerizeClusters(df_strategy, np.array(clusters), NCLUSTERS)
print(df_summerized)
sns.lineplot(data=df_forplotting, x='strategy',y='frequency',hue='cluster')


#%%

def sortCluster(df, target='Cluster', sortBy='Check'):

    if target not in df:
        print('[WARNING] There is no column named {}. Function retured None.'.format(target))
        return None

    tmp_df = DataFrame(columns=df.columns)

    for clusterID in range(NCLUSTERS):
        b = df[target] == clusterID
        tmp_Series = Series(df[b].mean(axis=0), name=clusterID, index=df.columns)
        tmp_df = tmp_df.append(tmp_Series,ignore_index=True)

    tmp_df = tmp_df.sort_values(sortBy)

    d = {}
    for i,item in enumerate(tmp_df[target]):
        d[item] = i

    return [d[x] for x in df[target]], tmp_df

#%%
df_strategy.insert(0,'Cluster',clusters)

#%%
clusters_sorted, df_summerized = sortCluster(df_strategy)
print(df_summerized)

#%%
# needs append because there is one extra row 
clusters_sorted.append(100)
df['Cluster_2'] = clusters_sorted

#%%
df.to_csv(PATH, index=None)

#%%
df.head()

#%%
