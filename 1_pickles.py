import pandas as pd
import pickle as pkl
import os

# List of files
sociotechnicalfiles = [
    'sociotechnicalCommentsCommits.csv',
    'sociotechnicalIssueCommits.csv',
    'sociotechnicalCommentsFiles.csv',
    'sociotechnicalIssueFiles.csv',
    'sociotechnicalCommentsLOC.csv',
    'sociotechnicalIssueLOC.csv',
    'socialHeroesCommentsWise.csv',
    'socialHeroesIssueWise.csv',
    'technicalHeroesCommitsWise.csv',
    'technicalHeroesFileWise.csv',
    'technicalHeroesLOCWise.csv',
    'technoSocialCommitCommentWise.csv',
    'technoSocialCommitIssueWise.csv',
    'technoSocialFileCommentsWise.csv',
    'technoSocialFileIssueWise.csv',
    'technoSocialLOCCommentsWise.csv',
    'technoSocialLOCIssueWise.csv',
    'superCommitsComments.csv',
    'superCommitIssues.csv',
    'superFileComments.csv',
    'superFileIssues.csv',
    'superLOCComments.csv',
    'superLOCIssues.csv'
]

# Directory paths (adjust if needed)
input_dir = "./"         # Folder containing the CSV files
output_dir = "./pickles" # Folder to save pickle files

# Create output folder if missing
os.makedirs(output_dir, exist_ok=True)

for file in sociotechnicalfiles:
    file_path = os.path.join(input_dir, file)

    # Read CSV
    df = pd.read_csv(file_path)

    # Build dictionary: project -> set of authors
    project_hero_dict = (
        df.groupby("Hero_Project_Name")["Hero Author Name"]
        .apply(set)
        .to_dict()
    )

    # Pickle file name
    pickle_name = file + ".pkl"
    pickle_path = os.path.join(output_dir, pickle_name)

    # Save as pickle
    with open(pickle_path, "wb") as f:
        pkl.dump(project_hero_dict, f)

    print(f"Saved: {pickle_path}")
