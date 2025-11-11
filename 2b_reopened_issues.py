import csv
import os
import pickle

import pandas as pd
from pymongo import MongoClient
from Build_reverse_identity_dictionary import Build_reverse_identity_dictionary
import time
import pickle as pkl
from datetime import timedelta
from collections import defaultdict
from bson import ObjectId


class Comparisons:
    def __init__(self):
        self.issue_project = dict()
        self.issue_start = dict()
        self.project_assignee_avg_time = dict()
        self.project_assignee_issue_time = dict()
        self.project_assignee_issue_date = dict()
        self.issue_assignee = dict()
        self.project_issue_author = dict()
        self.project_author_issue_dates = dict()
        self.project_author_issue_time = dict()
        self.project_author_avg_time = dict()
        self.BRID = Build_reverse_identity_dictionary()
        self.BRID.reading_identity_and_people_and_building_reverse_identity_dictionary()
        self.client = MongoClient("mongodb://localhost:27017/")  # Setting Up Connection with mongodb
        self.db = self.client['smartshark']  # Getting to the desired database
        self.file_name = self.db['event']  # Getting to the desired table/document
        self.records = list(self.file_name.find({}))  # Extracting all the records
        self.issue_issue_type = dict()
        self.issue_issue_priority = dict()
        self.issue_data = self.db["issue"]
        self.issue_records = list(self.issue_data.find({}, {}))
        self.issue_comments_data = self.db["issue_comment"]
        self.issue_comment_records = list(self.issue_comments_data.find({}, {}))
        self.minor_project_assignee_issue_date = dict()
        self.major_project_assignee_issue_date = dict()
        self.critical_project_assignee_issue_date = dict()
        self.trivial_project_assignee_issue_date = dict()
        self.blocker_project_assignee_issue_date = dict()
        self.bug_project_assignee_issue_date = dict()
        self.minor_project_assignee_issue_time = dict()
        self.major_project_assignee_issue_time = dict()
        self.critical_project_assignee_issue_time = dict()
        self.trivial_project_assignee_issue_time = dict()
        self.blocker_project_assignee_issue_time = dict()
        self.bug_project_assignee_issue_time = dict()
        self.minor_project_assignee_avg_time = dict()
        self.major_project_assignee_avg_time = dict()
        self.critical_project_assignee_avg_time = dict()
        self.trivial_project_assignee_avg_time = dict()
        self.blocker_project_assignee_avg_time = dict()
        self.bug_project_assignee_avg_time = dict()

    def build_issue_issue_types(self):
        self.issue_issue_type.clear()
        self.issue_issue_priority.clear()
        for element in self.issue_records:
            # print(element.keys())
            for key in element.keys():
                if key == 'priority':
                    issue = element["_id"]
                    issue_priority = element["priority"]
                    issue_types = element["issue_type"]
                    if issue_types == 'Bug':
                        if issue not in self.issue_issue_type.keys():
                            self.issue_issue_type[issue] = list()
                        if issue_types not in self.issue_issue_type[issue]:
                            self.issue_issue_type[issue].append(issue_types)
                    if issue not in self.issue_issue_priority.keys():
                        self.issue_issue_priority[issue] = list()
                    if issue_priority not in self.issue_issue_priority[issue]:
                        self.issue_issue_priority[issue].append(issue_priority)

    def loading_dictionaries(self):
        file_path2 = 'issue_project.pkl'
        with open(file_path2, 'rb') as file:
            self.issue_project = pkl.load(file)
        file_path3 = 'issue_start.pkl'
        with open(file_path3, 'rb') as file:
            self.issue_start = pkl.load(file)
        file_path5 = 'issue_assignee.pkl'
        with open(file_path5, 'rb') as file:
            issue_assignee1 = pkl.load(file)
        for i in issue_assignee1:
            if i not in self.issue_assignee.keys():
                self.issue_assignee[i] = list()
            if issue_assignee1[i] not in self.issue_assignee[i]:
                self.issue_assignee[i].append(issue_assignee1[i])

    def extracting_project_assignee_issue_date(self):
        results = dict()
        pickle_files = [
            'sociotechnicalCommentsCommits.csv.pkl',
            'sociotechnicalIssueCommits.csv.pkl',
            'sociotechnicalCommentsFiles.csv.pkl',
            'sociotechnicalIssueFiles.csv.pkl',
            'sociotechnicalCommentsLOC.csv.pkl',
            'sociotechnicalIssueLOC.csv.pkl',
            'socialHeroesCommentsWise.csv.pkl',
            'socialHeroesIssueWise.csv.pkl',
            'technicalHeroesCommitsWise.csv.pkl',
            'technicalHeroesFileWise.csv.pkl',
            'technicalHeroesLOCWise.csv.pkl',
            'technoSocialCommitCommentWise.csv.pkl',
            'technoSocialCommitIssueWise.csv.pkl',
            'technoSocialFileCommentsWise.csv.pkl',
            'technoSocialFileIssueWise.csv.pkl',
            'technoSocialLOCCommentsWise.csv.pkl',
            'technoSocialLOCIssueWise.csv.pkl',
            'superCommitsComments.csv.pkl',
            'superCommitIssues.csv.pkl',
            'superFileComments.csv.pkl',
            'superFileIssues.csv.pkl',
            'superLOCComments.csv.pkl',
            'superLOCIssues.csv.pkl'
        ]

        for pkl_file in pickle_files:
            project_assignee_map = dict()
            print(f"Processing: {pkl_file}")
            if not os.path.exists(pkl_file):
                print(f"Warning: {pkl_file} not found! Skipping...")
                continue

            # Load the pickle file
            with open(pkl_file, "rb") as f:
                data1 = pickle.load(f)

            if pkl_file not in results.keys():
                results[pkl_file] = dict()

            # Dictionary to store reopened percentages for this pickle
            bug_project_reopened = {}
            minor_project_reopened = {}
            major_project_reopened = {}
            critical_project_reopened = {}
            trivial_project_reopened = {}
            blocker_project_reopened = {}

            # Extract project-wise assignees
            project_assignee_map = {project: set(data1[project]) for project in
                                    data1}  # { project_name: set(assignees) }
            assignee_list = list()
            c = 0
            for pro in data1:
                for ass in data1[pro]:
                    if ass not in assignee_list:
                        assignee_list.append(ass)

            # Dictionary to track issue status changes
            bug_issue_status_history = defaultdict(
                lambda: defaultdict(list))  # { project_name: { issue_id: [(date, status, value)] } }
            minor_issue_status_history = defaultdict(
                lambda: defaultdict(list))
            major_issue_status_history = defaultdict(
                lambda: defaultdict(list))
            critical_issue_status_history = defaultdict(
                lambda: defaultdict(list))
            trivial_issue_status_history = defaultdict(
                lambda: defaultdict(list))
            blocker_issue_status_history = defaultdict(
                lambda: defaultdict(list))

            for elem in self.records:
                status = elem["status"].lower()
                if "new_value" in elem:
                    actual = str(elem["new_value"]).lower() if elem["new_value"] is not None else ""

                    issue = elem["issue_id"]
                    date = elem["created_at"]
                    if issue in self.issue_issue_priority:
                        # print(issue, self.issue_issue_priority[issue])
                        if issue in self.issue_assignee:
                            for assignee in self.issue_assignee[issue]:
                                assignee = self.BRID.reverse_identity_dict.get(assignee, assignee)
                                for project, assignees in project_assignee_map.items():
                                    if str(assignee) in assignees:
                                        # if self.issue_issue_type[issue] == ['Bug']:
                                        #     bug_issue_status_history[project][issue].append((date, status, actual))
                                        if self.issue_issue_priority[issue] == ['Minor']:
                                            minor_issue_status_history[project][issue].append((date, status, actual))
                                        if self.issue_issue_priority[issue] == ['Major']:
                                            major_issue_status_history[project][issue].append((date, status, actual))
                                        if self.issue_issue_priority[issue] == ['Critical']:
                                            critical_issue_status_history[project][issue].append((date, status, actual))
                                        if self.issue_issue_priority[issue] == ['Trivial']:
                                            trivial_issue_status_history[project][issue].append((date, status, actual))
                                        if self.issue_issue_priority[issue] == ['Blocker']:
                                            blocker_issue_status_history[project][issue].append((date, status, actual))

            for project, issues in minor_issue_status_history.items():
                total_issues = len(issues)
                reopened_issues = 0

                for issue, status_changes in issues.items():
                    status_changes.sort()  # Sort by date

                    fixed_index = None
                    for i, (_, status, new_value) in enumerate(status_changes):
                        if status == "resolution" and new_value == "fixed":
                            fixed_index = i
                        elif fixed_index is not None and status == "status" and new_value == "reopened":
                            reopened_issues += 1
                            break  # Stop checking once it's reopened

                # Calculate percentage
                reopened_percentage = (reopened_issues / total_issues) * 100 if total_issues > 0 else 0
                minor_project_reopened[project] = reopened_percentage

                # Print result
                print(
                    f"Minor Pickle: {pkl_file} | Project: {project} | {reopened_issues}/{total_issues} * 100 = {reopened_percentage:.2f}%")

            # Store this pickle file's results in a separate dictionary
            with open(f"{pkl_file}_reopened_issues_minor.pkl", 'wb') as f:
                pkl.dump(minor_project_reopened, f)

            for project, issues in major_issue_status_history.items():
                total_issues = len(issues)
                reopened_issues = 0

                for issue, status_changes in issues.items():
                    status_changes.sort()  # Sort by date

                    fixed_index = None
                    for i, (_, status, new_value) in enumerate(status_changes):
                        if status == "resolution" and new_value == "fixed":
                            fixed_index = i
                        elif fixed_index is not None and status == "status" and new_value == "reopened":
                            reopened_issues += 1
                            break  # Stop checking once it's reopened

                # Calculate percentage
                reopened_percentage = (reopened_issues / total_issues) * 100 if total_issues > 0 else 0
                major_project_reopened[project] = reopened_percentage

                # Print result
                print(
                    f"major_Pickle: {pkl_file} | Project: {project} | {reopened_issues}/{total_issues} * 100 = {reopened_percentage:.2f}%")

            # Store this pickle file's results in a separate dictionary
            with open(f"{pkl_file}_reopened_issues_major.pkl", 'wb') as f:
                pkl.dump(major_project_reopened, f)

            for project, issues in critical_issue_status_history.items():
                total_issues = len(issues)
                reopened_issues = 0

                for issue, status_changes in issues.items():
                    status_changes.sort()  # Sort by date

                    fixed_index = None
                    for i, (_, status, new_value) in enumerate(status_changes):
                        if status == "resolution" and new_value == "fixed":
                            fixed_index = i
                        elif fixed_index is not None and status == "status" and new_value == "reopened":
                            reopened_issues += 1
                            break  # Stop checking once it's reopened

                # Calculate percentage
                reopened_percentage = (reopened_issues / total_issues) * 100 if total_issues > 0 else 0
                critical_project_reopened[project] = reopened_percentage

                # Print result
                print(
                    f"critical_Pickle: {pkl_file} | Project: {project} | {reopened_issues}/{total_issues} * 100 = {reopened_percentage:.2f}%")

            # Store this pickle file's results in a separate dictionary
            with open(f"{pkl_file}_reopened_issues_critical.pkl", 'wb') as f:
                pkl.dump(critical_project_reopened, f)

            for project, issues in trivial_issue_status_history.items():
                total_issues = len(issues)
                reopened_issues = 0

                for issue, status_changes in issues.items():
                    status_changes.sort()  # Sort by date

                    fixed_index = None
                    for i, (_, status, new_value) in enumerate(status_changes):
                        if status == "resolution" and new_value == "fixed":
                            fixed_index = i
                        elif fixed_index is not None and status == "status" and new_value == "reopened":
                            reopened_issues += 1
                            break  # Stop checking once it's reopened

                # Calculate percentage
                reopened_percentage = (reopened_issues / total_issues) * 100 if total_issues > 0 else 0
                trivial_project_reopened[project] = reopened_percentage

                # Print result
                print(
                    f"trivial_Pickle: {pkl_file} | Project: {project} | {reopened_issues}/{total_issues} * 100 = {reopened_percentage:.2f}%")

            # Store this pickle file's results in a separate dictionary
            with open(f"{pkl_file}_reopened_issues_trivial.pkl", 'wb') as f:
                pkl.dump(trivial_project_reopened, f)

            for project, issues in blocker_issue_status_history.items():
                total_issues = len(issues)
                reopened_issues = 0

                for issue, status_changes in issues.items():
                    status_changes.sort()  # Sort by date

                    fixed_index = None
                    for i, (_, status, new_value) in enumerate(status_changes):
                        if status == "resolution" and new_value == "fixed":
                            fixed_index = i
                        elif fixed_index is not None and status == "status" and new_value == "reopened":
                            reopened_issues += 1
                            break  # Stop checking once it's reopened

                # Calculate percentage
                reopened_percentage = (reopened_issues / total_issues) * 100 if total_issues > 0 else 0
                blocker_project_reopened[project] = reopened_percentage

                # Print result
                print(
                    f"blocker_Pickle: {pkl_file} | Project: {project} | {reopened_issues}/{total_issues} * 100 = {reopened_percentage:.2f}%")

            # Store this pickle file's results in a separate dictionary
            with open(f"{pkl_file}_reopened_issues_blocker.pkl", 'wb') as f:
                pkl.dump(blocker_project_reopened, f)


if __name__ == "__main__":
    start_time = time.time()
    object1 = Comparisons()
    object1.build_issue_issue_types()
    object1.loading_dictionaries()
    object1.extracting_project_assignee_issue_date()

