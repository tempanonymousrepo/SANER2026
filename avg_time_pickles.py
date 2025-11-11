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

import pandas as pd
import pickle as pkl
from bson import ObjectId
from datetime import timedelta
import os

# List of files (total 23 files now)
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
severity = ['minor', 'major', 'critical', 'trivial', 'blocker']
for sev in severity:
    # Load the 'project_assignee_avg_time' dictionary
    file_path = f'{sev}_project_assignee_avg_time.pkl'
    with open(file_path, 'rb') as file:
        project_assignee_avg_time = pkl.load(file)

    # Function to get project average time
    def getting_project_avg_time(dict1):
        output = dict()
        for project in dict1:
            if project in project_assignee_avg_time:
                print(project)
                total_time = timedelta(days=0, seconds=0, microseconds=0)
                total_counter = 0
                for assignee in dict1[project]:
                    # print(f"assignee = {assignee} | {type(assignee)}")
                    if ObjectId(assignee) in project_assignee_avg_time[project]:
                        print("yes")
                        # print(ObjectId(assignee))
                        total_time += project_assignee_avg_time[project][ObjectId(assignee)]
                    total_counter += 1
                print(f"total time = {total_time} | total counter = {total_counter}")
                # Calculate the average time for the project (divide total time by the number of assignees)
                if total_counter > 0:
                    output[project] = total_time / total_counter
        return output


    # Initialize a list to hold the result for each file
    all_avg_times = []

    # Read all the CSV files and process
    for file in sociotechnicalfiles:
        df = pd.read_csv(file)
        # Group authors by project
        authors = df.groupby('Hero_Project_Name')['Hero Author Name'].apply(list).to_dict()

        # Get average time for the current file's data
        avg_times = getting_project_avg_time(authors)

        # Convert the average time to hours (for better readability)
        avg_times_in_hours = {project: avg_time.total_seconds() / 3600 for project, avg_time in avg_times.items()}

        # Append the result (list of average times for the projects) to the all_avg_times list
        all_avg_times.append(avg_times_in_hours)

        # Save the average times into a pickle file with the same base name as the original file
        base_name = os.path.basename(file)  # Get the base name of the file
        file_name_without_ext = os.path.splitext(base_name)[0]  # Remove file extension
        output_pickle_file = f'{sev}_{file_name_without_ext}_avg_time.pkl'  # Create the pickle file name

        # Save the pickle file
        with open(output_pickle_file, 'wb') as f:
            pkl.dump(avg_times_in_hours, f)

