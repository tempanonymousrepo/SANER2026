import itertools
import pandas as pd

# Load the square matrix
df = pd.read_csv("final_mean_jaccard_matrix.csv", index_col=0)

# Prepare a list of unique (i, j) pairs from the lower triangle (excluding diagonal)
pairs = []
for i, j in itertools.combinations(df.columns, 2):
    pairs.append({
        "Pair": f"{i} - {j}",
        "Value": df.loc[i, j]
    })

# Convert to DataFrame
pairs_df = pd.DataFrame(pairs)

# Sort by Value (descending)
pairs_df = pairs_df.sort_values(by="Value", ascending=False).reset_index(drop=True)

# Save to CSV
pairs_df.to_csv("jaccard_pairs_sorted.csv", index=False)

print("Saved as 'jaccard_pairs_sorted.csv'")
print(pairs_df.head())


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ── Load matrix ───────────────────────────────────────────────
df = pd.read_csv("final_mean_jaccard_matrix.csv", index_col=0)
df = df.astype(float)

# ── Common vmin/vmax across all plots ─────────────────────────
vmin = df.min().min()
vmax = df.max().max()

# ── Mask upper triangle (keep lower) ──────────────────────────
mask = np.triu(np.ones_like(df, dtype=bool), k=1)

# ── Define clusters ───────────────────────────────────────────
clusters = {
    "ST": ["ST1", "ST2", "ST3", "ST4", "ST5", "ST6"],
    "S": ["S1", "S2"],
    "T": ["T1", "T2", "T3"],
    "TS": ["TS1", "TS2", "TS3", "TS4", "TS5", "TS6"],
    "SH": ["SH1", "SH2", "SH3", "SH4", "SH5", "SH6"]
}

# ── Helper function: draw and save heatmap ─────────────────────
def plot_lower_triangle(data, mask, filename, s, fs, highlight_cluster=None, annotate=False, show_cbar=True):
    plt.figure(figsize=(10, 10))
    ax = sns.heatmap(
        data,
        mask=mask,
        cmap="coolwarm",
        vmin=vmin,
        vmax=vmax,
        annot=annotate,                # toggle annotation
        fmt=".3f",
        annot_kws={"size": s, "weight": "bold"},
        square=True,
        cbar=show_cbar,
        cbar_kws={
            "shrink": 0.8,
            "aspect": 130,
            "pad": 0.04,
            "orientation": "vertical",
            "location": "left"
        },
        linewidths=0,
        linecolor=None
    )

    # Make upper triangle white
    ax.imshow(
        np.ones_like(data),
        cmap="Greys",
        alpha=mask.astype(float),
        zorder=2,
        extent=(0, data.shape[1], 0, data.shape[0]),
        origin="lower"
    )

    # Tick labels
    ax.xaxis.tick_bottom()
    ax.yaxis.tick_left()
    ax.tick_params(axis='x', rotation=0, labelsize=fs)
    ax.tick_params(axis='y', rotation=0, labelsize=fs)
    ax.set_xticklabels(ax.get_xticklabels(), fontweight="bold")
    ax.set_yticklabels(ax.get_yticklabels(), fontweight="bold")

    # Optional yellow borders (for all or specific cluster)
    for cname, labels in clusters.items():
        if highlight_cluster and cname != highlight_cluster:
            continue  # only draw selected cluster
        indices = [i for i, label in enumerate(data.columns) if label in labels]
        if indices:
            min_idx, max_idx = min(indices), max(indices)
            ax.plot([min_idx, max_idx + 1], [max_idx + 1, max_idx + 1],
                    color='yellow', lw=2, zorder=3)
            ax.plot([min_idx, min_idx], [min_idx, max_idx + 1],
                    color='yellow', lw=2, zorder=3)

    plt.tight_layout()
    plt.savefig(filename, format="png", bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Saved: {filename}")

# ── 2️ T cluster (annotated) ────────────────────────────────────────
t_indices = [i for i, lbl in enumerate(df.columns) if lbl in clusters["T"]]
t_df = df.iloc[t_indices, t_indices]
t_mask = np.triu(np.ones_like(t_df, dtype=bool), k=1)
plot_lower_triangle(t_df, t_mask, "jaccard_lower_triangle_T.png", 30, 30, highlight_cluster="T", annotate=True, show_cbar=False)

# ── 3️ S cluster (annotated) ─────────────────────────────────────────
s_indices = [i for i, lbl in enumerate(df.columns) if lbl in clusters["S"]]
s_df = df.iloc[s_indices, s_indices]
s_mask = np.triu(np.ones_like(s_df, dtype=bool), k=1)
plot_lower_triangle(s_df, s_mask, "jaccard_lower_triangle_S.png", 40, 40, highlight_cluster="S", annotate=True, show_cbar=False)


import pandas as pd
import numpy as np

# Load matrix
df = pd.read_csv("final_mean_jaccard_matrix.csv", index_col=0).astype(float)

# Define clusters
clusters = {
    "ST": ["ST1", "ST2", "ST3", "ST4", "ST5", "ST6"],
    "S": ["S1", "S2"],
    "T": ["T1", "T2", "T3"],
    "TS": ["TS1", "TS2", "TS3", "TS4", "TS5", "TS6"],
    "SH": ["SH1", "SH2", "SH3", "SH4", "SH5", "SH6"]
}

# Prepare result matrix
cluster_names = list(clusters.keys())
cluster_matrix = pd.DataFrame(index=cluster_names, columns=cluster_names, dtype=float)

# Compute means
for c1 in cluster_names:
    for c2 in cluster_names:
        sub_df = df.loc[clusters[c1], clusters[c2]]

        if c1 == c2:
            # Exclude diagonal self-comparisons
            mask = ~np.eye(sub_df.shape[0], dtype=bool)
            values = sub_df.values[mask]
        else:
            # Use all pairwise comparisons between different clusters
            values = sub_df.values.flatten()

        cluster_matrix.loc[c1, c2] = np.mean(values)

# Save
cluster_matrix.to_csv("cluster_level_mean_jaccard_matrix.csv", float_format="%.4f")
print("Saved 'cluster_level_mean_jaccard_matrix.csv'")
mask = np.triu(np.ones_like(cluster_matrix, dtype=bool), k=1)
# Plot the 6×6 cluster heatmap
plt.figure(figsize=(6, 3))
ax = sns.heatmap(
    cluster_matrix.astype(float),
    annot=True,
    fmt=".3f",
    cmap="coolwarm",
    mask=mask,
    square=False,
    cbar_kws={"shrink": 1.0, "aspect": 10, "pad": 0.02},
    linewidths=0.3,
    linecolor="white",
    annot_kws={"size": 7, "weight": "bold"}
)

# Flatten vertically
ax.set_aspect(0.5)

# Tick styling
ax.set_xticklabels(ax.get_xticklabels(), fontweight="bold", fontsize=7)
ax.set_yticklabels(ax.get_yticklabels(), fontweight="bold", fontsize=7)

plt.tight_layout()
plt.savefig("cluster_level_mean_jaccard_heatmap.pdf", format="pdf", bbox_inches="tight", dpi=300)
plt.savefig("cluster_level_mean_jaccard_heatmap.png", format="png", bbox_inches="tight", dpi=300)
plt.show()



