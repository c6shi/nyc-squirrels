import pandas as pd
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

behaviors = [
    'indifferent', 'runs_from',
    'running', 'climbing', 'eating', 'foraging',
    'tail_twitches']

features = ['nearbuilding', 'neargarden', 'neargrass', 'nearpedestrian', 'nearwater', 'nearwoods']

stats_rows = []

sqrls = pd.read_csv('dataframes/bfsqrlspd.csv')
sqrls = sqrls.drop(columns='Unnamed: 0')


def permutation_test(b, f1, f2):
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

    fig = Figure()
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.set_title(
        'Distribution of the absolute difference in proportion of squirrels\nexhibiting the ' +
        '{0} behavior near {1} versus near {2}'.format(b, f1[4:], f2[4:]),
        wrap=True
    )
    ax.get_xticklabels()
    ax.hist(stats, density=True)
    ax.axvline(observed_stat, color='red')
    fig.savefig('histograms/{0}/{1}_{2}.png'.format(b, f1, f2), bbox_inches='tight')

    p_value = np.mean(stats >= observed_stat)
    stats_rows.append([b, f1, f2, p_value])
    return


for b in behaviors[3:]:
    for i in range(len(features)):
        for j in range(i+1, len(features)):
            permutation_test(b, features[i], features[j])


stats_df = pd.DataFrame(stats_rows)
stats_df.columns = ['behavior', 'feature 1', 'feature 2', 'p-value']
stats_df.to_csv("dataframes/permutation_results.csv")
