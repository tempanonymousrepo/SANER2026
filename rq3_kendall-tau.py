import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr
import rbo  # Importing rbo library

# Define the rankings
rankings = {
    # # Fixed
    "Trivial": ["SH1", "SH2", "SH3", "SH4", "TS3", "TS4", "T3", "TS1", "TS2", "T2", "ST3", "ST1", "ST6", "S1", "ST2", "S2", "ST5", "ST4", "SH6", "TS5", "T1", "SH5", "TS6"],
    "Minor": ["TS3", "TS4", "SH3", "T2", "SH4", "TS2", "TS1", "SH1", "T3", "SH2", "ST3", "ST6", "ST1", "ST2", "S1", "ST5", "S2", "ST4", "TS5", "SH5", "TS6", "SH6", "T1"],
    "Major": ["SH4", "TS4", "SH3", "TS3", "T2", "SH2", "TS2", "SH1", "TS1", "T3", "ST3", "ST1", "ST6", "S2", "ST2", "TS5", "S1", "ST5", "ST4", "SH6", "SH5", "T1", "TS6"],
    "Critical": ["TS5", "TS2", "SH1", "SH2", "TS4", "T3", "TS1", "SH3", "TS3", "ST4", "T2", "SH4", "ST5", "ST1", "ST2", "ST3", "ST6", "S1", "SH5", "TS6", "S2", "T1", "SH6"],
    "Blocker": ["T3", "TS1", "T2", "TS3", "SH2", "TS2", "SH1", "TS4", "SH3", "SH4", "S1", "ST3", "ST1", "ST6", "ST2", "S2", "T1", "ST4", "ST5", "TS5", "TS6", "SH5", "SH6"]

    # # Reopened
    # "Trivial": ["T2", "SH3", "TS3", "TS4", "SH4", "T3", "TS1", "TS2", "SH1", "SH2", "S2", "S1",
    #             "ST2", "ST6", "ST1", "ST3", "ST5", "ST4", "SH5", "TS5", "TS6", "SH6", "T1"],
    # "Minor": ["SH1", "S2", "SH2", "T3", "TS1", "TS2", "S1", "ST2", "ST6", "ST3", "ST1", "SH3", "SH4",
    #           "T2", "TS3", "TS4", "TS5", "TS6", "SH5", "SH6", "ST4", "ST5", "T1"],
    # "Major": ["SH4", "T2", "SH3", "TS3", "TS4", "T3", "TS1", "SH2", "SH1", "TS2", "ST6", "S2", "ST2",
    #           "S1", "ST3", "ST1", "TS5", "T1", "TS6", "ST4", "ST5", "SH5", "SH6"],
    # "Critical": ["SH1", "SH2", "TS1", "TS2", "T3", "SH3", "SH4", "TS3", "TS4", "T2", "S2", "ST6", "ST2",
    #              "ST3", "ST1", "S1", "ST5", "ST4", "T1", "SH5", "SH6", "TS5", "TS6"],
    # "Blocker": ["ST1", "ST3", "TS3", "TS4", "SH3", "SH4", "T2", "ST2", "ST6", "SH1", "TS1", "TS2", "SH2",
    #             "T3", "S2", "S1", "TS5", "TS6", "SH6", "SH5", "ST5", "ST4", "T1"]
}

# Compute correlation matrices
keys = list(rankings.keys())
n = len(keys)

kendall_matrix = np.zeros((n, n), dtype=float)
kendall_p_matrix = np.zeros((n, n), dtype=float)

for i in range(n):
    for j in range(n):
        tau, p_tau = kendalltau(rankings[keys[i]], rankings[keys[j]])

        kendall_matrix[i, j] = tau
        kendall_p_matrix[i, j] = p_tau

# Convert results to DataFrames
kendall_df = pd.DataFrame(kendall_matrix, index=keys, columns=keys)

# Format the correlation matrices with p-values
formatted_kendall = kendall_df.round(3).astype(str) + " (" + pd.DataFrame(kendall_p_matrix, index=keys, columns=keys).round(3).astype(str) + ")"

# Save to CSV files
formatted_kendall.to_csv("fixed_kendall_tau.csv", index=True)

print("Saved Kendall's Tau results to CSV files.")
