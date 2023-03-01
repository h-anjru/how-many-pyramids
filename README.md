# how-many-pyramids

Determine how many checkpoints are needed to achieve a certain level of accuracy.

## Overview

This script takes as input a CSV of discrepencies or errors, such as those one would find among checkpoints. The script iterates through all combinations of size *m* through *n* of these checkpoints and calculates basic summary statistics for each combination. Each combo set is then itself summarized.

## User input

All the user input needed is at hte beginning of the script:

```py
### USER INPUT ###
infile = 'deltas_starnet.csv'
m = 2
n = 24
### END USER INPUT ###
```

The input file should be as CSV with a header row, formatted as `name, delta_easting, delta_northing, delta_height`, for example:

```
pyramid,dE,dN,dH
1,-0.021,0.025,-0.018
2,0.008,-0.037,0.021
3,0.009,0.005,-0.008
4,0.023,-0.013,0.004
5,-0.017,-0.069,0.021
...
```

As stated above, the script iterates through all combinations of size *m* through *n* of these checkpoints' errors (or, more precisely, discrepencies) and calculates basic summary statistics.

## Output
The output of the script is a series of CSV files that are saved in a new directory with the same name as the input file. Perhaps most important of all output is the CSV file whose name begins with `overall`, which contains the 5th, 50th, and 95th percentiles of the means and RMSEs for all statistics for combinations of sizes *m* through *n*.

## Dependencies
This script requires the following external libraries:

- **NumPy**: [NumPy user guide](https://numpy.org/doc/stable/)
- **pandas**: [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html)
