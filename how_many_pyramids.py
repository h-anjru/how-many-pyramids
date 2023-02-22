import itertools
import numpy as np
import os
import pandas as pd

"""
Objective: Determine how many checkpoints are needed to achieve a certain level of accuracy.

This script takes as input a CSV of discrepencies or errors, such as those one would find among checkpoints. The script 
iterates through all combinations of size m through n of these checkpoints and calculates basic summary statistics for 
each combination. Each combo set is then itself summarized.
"""

### USER INPUT ###
infile = 'deltas_starnet.csv'
m = 2
n = 2
### END USER INPUT ###

df_in = pd.read_csv(infile)

# iterate through dataframe for combinations
for ii in range(m, n + 1):
    # subset is a tuple of integers to be used as row indices
    for subset in itertools.combinations(range(len(df_in.index)), ii):
        # np.r_[] allows a call to non-consecutive ranges
        combo = df_in.iloc[np.r_[subset]]

        # stats on this combo as dict (to append to df_out)
        names = combo['pyramid'].tolist()

        stats = {
            'combo': ','.join([str(value) for value in names]),
            'mean_dE': round(combo['dE'].mean(), 5),
            'mean_dN': round(combo['dN'].mean(), 5),
            'mean_dH': round(combo['dH'].mean(), 5),
            'stdev_dE': round(combo['dE'].std(), 5),
            'stdev_dN': round(combo['dN'].std(), 5),
            'stdev_dH': round(combo['dH'].std(), 5),
            'SE_dE': round(combo['dE'].std() / (len(combo) + 1) ** 0.5, 5),
            'SE_dN': round(combo['dN'].std() / (len(combo) + 1) ** 0.5, 5),
            'SE_dH': round(combo['dH'].std() / (len(combo) + 1) ** 0.5, 5),
            'rmse_dE': round(((combo['dE'] ** 2).sum() / ii) ** 0.5, 5),
            'rmse_dN': round(((combo['dN'] ** 2).sum() / ii) ** 0.5, 5),
            'rmse_dH': round(((combo['dH'] ** 2).sum() / ii) ** 0.5, 5),
        }

        # from dict to df
        stats_df = pd.DataFrame([stats])

        # append current combo's stats to output df
        try:
            df_out = pd.concat([df_out, stats_df], ignore_index=True)
        except NameError:  # df_out not yet created
            df_out = pd.DataFrame(columns=list(stats.keys()))
            df_out = pd.concat([df_out, stats_df], ignore_index=True)

    # send current dataframe for all combos of size ii to csv
    # save output
    path_to_output = infile[:-4]
    if not os.path.exists(path_to_output):
        os.makedirs(path_to_output)

    df_out.to_csv(os.path.join(path_to_output, f'combos_{ii}.csv'))

    # clear df_out to begin new output
    del df_out

# open each "combos" output CSV
path = os.path.join(os.getcwd(), path_to_output)

filenames = []

for file in os.listdir(path):
    filename = os.fsdecode(file)
    if filename.startswith('combos_'):
        filenames.append(filename)
    else:
        continue

for file in filenames:
    df = pd.read_csv(os.path.join(path, file))

    # stats on this combo as dict (to append to df_out)
    for col in df.columns[2:]:
        stats = {
            'stat': col,
            'mean': round(df[col].mean(), 5),
            'stdev': round(df[col].std(), 5),
            'SEOM':  round(df[col].std() / (len(df) + 1) ** 0.5, 5),
            'RMSE': round(((df[col] ** 2).sum() / len(df)) ** 0.5, 5),
            '05th': round(df[col].quantile(0.05), 5),
            '50th': round(df[col].quantile(0.50), 5),
            '95th': round(df[col].quantile(0.95), 5),
        }

        # from dict to df
        stats_df = pd.DataFrame([stats])

        # append current combo's stats to output df
        try:
            df_out = pd.concat([df_out, stats_df], ignore_index=True)
        except NameError:  # df_out not yet created
            df_out = pd.DataFrame(columns=list(stats.keys()))
            df_out = pd.concat([df_out, stats_df], ignore_index=True)

    # send current dataframe for all combos of size ii to csv
    df_out.to_csv(os.path.join(path, f'summary_{file}'))

    # clear df_out to begin new output
    del df_out


# open each "summary" output CSV
path = os.path.join(os.getcwd(), path_to_output)

filenames = []

for file in os.listdir(path):
    filename = os.fsdecode(file)
    if filename.startswith('summary_'):
        filenames.append(filename)
    else:
        continue

for file in filenames:
    df = pd.read_csv(os.path.join(path, file))

    # stats on this combo as dict (to append to df_out)
    for index, row in df.iterrows():
        if row['stat'].startswith('mean') or row['stat'].startswith('rmse'):
            stats = {
                'combos_of': file[-5],
                'stat': row['stat'],
                '05th': row['05th'],
                '50th': row['50th'],
                '95th': row['95th'],
            }

            # from dict to df
            stats_df = pd.DataFrame([stats])

            # append current combo's stats to output df
            try:
                df_out = pd.concat([df_out, stats_df], ignore_index=True)
            except NameError:  # df_out not yet created
                df_out = pd.DataFrame(columns=list(stats.keys()))
                df_out = pd.concat([df_out, stats_df], ignore_index=True)

# send current dataframe for all combos of size ii to csv
df_out.to_csv(os.path.join(path, f'overall_{file}'))

# clear df_out to begin new output
del df_out
