import statistics

from sk import Rx
import pickle
import os

# Define all pickle file groups
# severity = [
#     'csv.pkl_reopened_issues',
#     'csv.pkl_reopened_issues_minor', 'csv.pkl_reopened_issues_major', 'csv.pkl_reopened_issues_critical',
#     'csv.pkl_reopened_issues_trivial', 'csv.pkl_reopened_issues_blocker'
# ]
severity = [
    'csv.pkl_fixed_issues',
    'csv.pkl_fixed_issues_minor', 'csv.pkl_fixed_issues_major', 'csv.pkl_fixed_issues_critical',
    'csv.pkl_fixed_issues_trivial', 'csv.pkl_fixed_issues_blocker'
]
for sev in severity:
    pickle_files = [
        f"superLOCIssues.{sev}.pkl",
        f"superLOCComments.{sev}.pkl",
        f"superFileIssues.{sev}.pkl",
        f"superFileComments.{sev}.pkl",
        f"superCommitIssues.{sev}.pkl",
        f"superCommitsComments.{sev}.pkl",
        f"technoSocialLOCIssueWise.{sev}.pkl",
        f"technoSocialLOCCommentsWise.{sev}.pkl",
        f"technoSocialFileIssueWise.{sev}.pkl",
        f"technoSocialFileCommentsWise.{sev}.pkl",
        f"technoSocialCommitIssueWise.{sev}.pkl",
        f"technoSocialCommitCommentWise.{sev}.pkl",
        f"sociotechnicalCommentsLOC.{sev}.pkl",
        f"sociotechnicalCommentsCommits.{sev}.pkl",
        f"sociotechnicalCommentsFiles.{sev}.pkl",
        f"sociotechnicalIssueLOC.{sev}.pkl",
        f"sociotechnicalIssueFiles.{sev}.pkl",
        f"sociotechnicalIssueCommits.{sev}.pkl",
        f"technicalHeroesLOCWise.{sev}.pkl",
        f"technicalHeroesFileWise.{sev}.pkl",
        f"technicalHeroesCommitsWise.{sev}.pkl",
        f"socialHeroesIssueWise.{sev}.pkl",
        f"socialHeroesCommentsWise.{sev}.pkl"
    ]

    # Map h1, h2, ..., h23 to corresponding pickle files
    label_mapping = {f"h{i+1}": pickle_files[i] for i in range(len(pickle_files))}

    # Load all pickles and find common projects
    all_data = {}
    project_sets = []  # Track projects in each pickle
    valid_labels = []  # Track labels for found pickle files

    for i, pkl_file in enumerate(pickle_files):
        if not os.path.exists(pkl_file):
            print(f"Warning: {pkl_file} not found! Skipping...")
            continue

        # Load the pickle file
        with open(pkl_file, "rb") as f:
            data1 = pickle.load(f)  # Expecting a dictionary {project_name: avg_time}

        data = {k: v for k, v in data1.items() if v != 0.0}
        project_sets.append(set(data.keys()))

        # Store loaded data
        label = f"h{i+1}"
        all_data[label] = data
        valid_labels.append(label)  # Track valid labels

    if not project_sets:
        print(f"No valid data found for severity {sev}. Skipping...\n")
        continue

    # Get the set of projects that are common across all pickle files
    common_projects = set.intersection(*project_sets)

    # Sort project names for consistency
    sorted_common_projects = sorted(common_projects)

    # Create the final dictionary with only common projects
    final_data = {
        label: [all_data[label][proj] for proj in sorted_common_projects]
        for label in valid_labels
    }

    # Compute means and sort by mean values
    mean_values = {label: statistics.mean(values) for label, values in final_data.items()}
    sorted_means = sorted(mean_values.items(), key=lambda x: x[1])  # Sort by mean

    # Print results
    print(sev)
    for label, mean in sorted_means:
        print(label, label_mapping[label], mean)
    sorted_meansd = sorted(mean_values.items(), key=lambda x: x[1], reverse=False)
    for label, mean in sorted_meansd:
        print(mean)
    print(f"----------------------------------------------------------------------------------------------------\n")
