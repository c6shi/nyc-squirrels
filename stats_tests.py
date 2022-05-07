import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_cleaning import behaviors
from buffer_analysis import geospatial_analysis as features

sqrls = pd.read_csv('dataframes/bfsqrls.csv')
sqrls = sqrls.drop(columns='Unnamed: 0')

stats_rows = []

for b in behaviors:
    for i in range(len(features)):
        f1 = features[i]
        for j in range(i + 1, len(features)):
            f2 = features[j]
            behavior_df = sqrls[[b, f1, f2]]
            grouped = behavior_df.groupby(behavior_df[b]).sum()
            grouped = grouped.divide(grouped.sum(axis=0), axis=1)
            observed_stat = abs(grouped.loc[1][1] - grouped.loc[1][0])

            stats = np.array([])

            for i in range(10000):
                shuffled = behavior_df[b].sample(frac=1).reset_index(drop=True)
                shuffled_df = behavior_df.assign(**{'shuffled ' + b: shuffled})
                shuffled_grouped = shuffled_df.groupby('shuffled ' + b).sum()
                shuffled_grouped = shuffled_grouped.divide(shuffled_grouped.sum(axis=0), axis=1)
                shuffled_stat = abs(shuffled_grouped.loc[1][2] - shuffled_grouped.loc[1][1])
                stats = np.append(stats, shuffled_stat)

            plt.hist(stats)
            plt.axvline(observed_stat, color='red')
            plt.show()

            p_value = np.mean(stats >= observed_stat)
            stats_rows.append([b, f1, f2, p_value])

stats_df = pd.DataFrame(stats_rows)
stats_df.columns = ['behavior', 'feature 1', 'feature 2', 'p-value']
