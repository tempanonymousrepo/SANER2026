import time
from pymongo import MongoClient
from identity_merging.Build_reverse_identity_dictionary import Build_reverse_identity_dictionary


class TechnicalHeroes_data:
    def __init__(self):
        self.BRID = Build_reverse_identity_dictionary()
        self.BRID.reading_identity_and_people_and_building_reverse_identity_dictionary()
        self.project_author_commits_count = dict()
        self.project_committer_commits_count = dict()
        self.sorted_project_author_commits_count = dict()
        self.sorted_project_committer_commits_count = dict()
        self.sorted_project_author_loc_count = dict()
        self.sorted_project_committer_loc_count = dict()
        self.sorted_project_author_total_file_count = dict()
        self.sorted_project_committer_total_file_count = dict()
        self.sorted_project_author_unique_file_count = dict()
        self.sorted_project_committer_unique_file_count = dict()
        self.project_technical_heroes_based_on_authors_number_of_commits = dict()
        self.project_technical_heroes_based_on_committers_number_of_commits = dict()
        self.project_technical_heroes_based_on_authors_number_of_loc = dict()
        self.project_technical_heroes_based_on_committers_number_of_loc = dict()
        self.project_technical_heroes_based_on_authors_number_of_total_file = dict()
        self.project_technical_heroes_based_on_committers_number_of_total_file = dict()
        self.project_technical_heroes_based_on_authors_number_of_unique_file = dict()
        self.project_technical_heroes_based_on_committers_number_of_unique_file = dict()
        self.project_Author_loc_count = dict()
        self.project_Committer_loc_count = dict()
        self.project_Author_unique_file_count = dict()
        self.project_Author_unique_file_list = dict()
        self.project_Author_total_file_count = dict()
        self.project_Author_total_file_list = dict()
        self.project_Committer_total_file_count = dict()
        self.project_Committer_total_file_list = dict()
        self.project_Committer_unique_file_count = dict()
        self.project_Committer_unique_file_list = dict()
        self.project_Author_commits_list = dict()
        self.project_Committer_commits_list = dict()
        self.project_list_of_commits = dict()
        self.project_total_commits_count = dict()
        self.project_total_loc_count = dict()
        self.project_unique_file_count = dict()
        self.project_total_file_count = dict()
        self.commits_set_of_files = dict()
        self.commits_loc_count = dict()
        self.commits_project_dictionary = dict()
        self.commits_author_dictionary = dict()
        self.commits_committer_dictionary = dict()
        self.set_of_projects = list()
        self.set_of_authors = list()
        self.set_of_commits_master = list()
        self.set_of_commits_file_action = list()
        self.set_of_commits_master_refined = list()
        self.set_of_committers = list()
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["smartshark"]
        self.comment_data = self.db["comments_with_issue_and_project_info"]
        self.commit_data = self.db["commit_with_project_info"]
        self.commit_file_data = self.db["file_action"]
        self.commit_records = list(self.commit_data.find({}))
        self.commit_file_records = list(self.commit_file_data.find({}))
        self.project_set_of_authors = dict()
        self.project_set_of_committers = dict()

    def commit_author_committer_project_dictionary_set_of_commits_etc(self):
        for elem_l in self.commit_file_records:
            commit = elem_l["commit_id"]
            self.set_of_commits_file_action.append(commit)
        self.set_of_commits_file_action = list(dict.fromkeys(self.set_of_commits_file_action))

        for list_elem in self.commit_records:
            commit_id = list_elem["_id"]
            project = list_elem["project_name_info"]["name"]
            author = self.BRID.reverse_identity_dict[list_elem["author_id"]]
            committer = self.BRID.reverse_identity_dict[list_elem["committer_id"]]
            if project not in self.project_set_of_authors.keys():
                self.project_set_of_authors[project] = list()
            if project not in self.project_set_of_committers.keys():
                self.project_set_of_committers[project] = list()
            if author not in self.project_set_of_authors[project]:
                self.project_set_of_authors[project].append(author)
            if committer not in self.project_set_of_committers[project]:
                self.project_set_of_committers[project].append(committer)

            self.set_of_commits_master.append(commit_id)

            self.set_of_authors.append(author)
            self.set_of_committers.append(committer)
            self.set_of_projects.append(project)
            self.commits_project_dictionary[commit_id] = project
            self.commits_author_dictionary[commit_id] = author
            self.commits_committer_dictionary[commit_id] = committer

        self.set_of_authors = list(dict.fromkeys(self.set_of_authors))

        self.set_of_committers = list(dict.fromkeys(self.set_of_committers))

        self.set_of_projects = list(dict.fromkeys(self.set_of_projects))

    def build_project_list_of_commits_dictionary(self):

        for list_elem in self.commit_records:
            project = list_elem["project_name_info"]["name"]

            commit = list_elem["_id"]
            if project not in self.project_list_of_commits:
                self.project_list_of_commits[project] = list()
                self.project_list_of_commits[project].append(commit)
            else:
                self.project_list_of_commits[project].append(commit)

    def build_project_total_commit_lOC_and_file_count_dictionary(self):
        for project in self.set_of_projects:
            self.project_total_commits_count[project] = len(self.project_list_of_commits[project])

            var_project_loc_count = 0
            var_project_unique_file_count = 0
            var_project_total_file_count = 0

            list_of_commits = self.project_list_of_commits[project]

            for commit in list_of_commits:
                if commit in self.commits_loc_count:
                    var_project_loc_count = var_project_loc_count + self.commits_loc_count[commit]
                if commit in self.commits_set_of_files:
                    var_project_total_file_count = var_project_total_file_count + len(self.commits_set_of_files[commit])
                    var_project_unique_file_count = var_project_unique_file_count + len(
                        list(dict.fromkeys(self.commits_set_of_files[commit])))
            self.project_total_loc_count[project] = var_project_loc_count
            self.project_total_file_count[project] = var_project_total_file_count
            self.project_unique_file_count[project] = var_project_unique_file_count

    def build_project_author_and_committer_list_of_commits_dictionary(self):

        for list_elem in self.commit_records:
            project = list_elem["project_name_info"]["name"]
            author1 = self.BRID.reverse_identity_dict[list_elem["author_id"]]
            committer = self.BRID.reverse_identity_dict[list_elem["committer_id"]]
            commit = list_elem["_id"]

            if project not in self.project_Author_commits_list:
                self.project_Author_commits_list[project] = dict()
            if author1 not in self.project_Author_commits_list[project]:
                self.project_Author_commits_list[project][author1] = list()
            if commit not in self.project_Author_commits_list[project][author1]:
                self.project_Author_commits_list[project][author1].append(commit)
            if project not in self.project_Committer_commits_list:
                self.project_Committer_commits_list[project] = dict()
            if committer not in self.project_Committer_commits_list[project]:
                self.project_Committer_commits_list[project][committer] = list()
            if commit not in self.project_Committer_commits_list[project][committer]:
                self.project_Committer_commits_list[project][committer].append(commit)

    def build_project_author_and_committer_lOC_and_file_count_dictionary_initialization(self):
        for project in self.set_of_projects:
            if project not in self.project_Committer_loc_count:
                self.project_Committer_loc_count[project] = dict()
            if project not in self.project_Author_loc_count:
                self.project_Author_loc_count[project] = dict()
            if project not in self.project_Committer_total_file_count:
                self.project_Committer_total_file_count[project] = dict()
                self.project_Committer_total_file_list[project] = dict()
            if project not in self.project_Author_total_file_count:
                self.project_Author_total_file_count[project] = dict()
                self.project_Author_total_file_list[project] = dict()
            if project not in self.project_Committer_unique_file_count:
                self.project_Committer_unique_file_count[project] = dict()
                self.project_Committer_unique_file_list[project] = dict()
            if project not in self.project_Author_unique_file_count:
                self.project_Author_unique_file_count[project] = dict()
                self.project_Author_unique_file_list[project] = dict()
            for committer in self.set_of_committers:
                if committer not in self.project_Committer_loc_count[project]:
                    self.project_Committer_loc_count[project][committer] = 0
                if committer not in self.project_Committer_total_file_list[project]:
                    self.project_Committer_total_file_list[project][committer] = list()
                if committer not in self.project_Committer_total_file_count[project]:
                    self.project_Committer_total_file_count[project][committer] = 0
                if committer not in self.project_Committer_unique_file_count[project]:
                    self.project_Committer_unique_file_count[project][committer] = 0
                if committer not in self.project_Committer_unique_file_list[project]:
                    self.project_Committer_unique_file_list[project][committer] = list()
            for author in self.set_of_authors:
                if author not in self.project_Author_loc_count[project]:
                    self.project_Author_loc_count[project][author] = 0
                if author not in self.project_Author_total_file_count[project]:
                    self.project_Author_total_file_count[project][author] = 0
                if author not in self.project_Author_total_file_list[project]:
                    self.project_Author_total_file_list[project][author] = list()
                if author not in self.project_Author_unique_file_count[project]:
                    self.project_Author_unique_file_count[project][author] = 0
                if author not in self.project_Author_unique_file_list[project]:
                    self.project_Author_unique_file_list[project][author] = list()

    def build_project_author_and_committer_lOC_and_file_count_dictionary(self):
        for commit in self.set_of_commits_file_action:
            project_for_current_commit = self.commits_project_dictionary[commit]
            author_for_current_commit = self.commits_author_dictionary[commit]
            committer_for_current_commit = self.commits_committer_dictionary[commit]
            loc_count_for_current_commit = self.commits_loc_count[commit]
            files_for_current_commit = self.commits_set_of_files[commit]
            self.project_Author_loc_count[project_for_current_commit][author_for_current_commit] = \
                self.project_Author_loc_count[project_for_current_commit][
                    author_for_current_commit] + loc_count_for_current_commit
            self.project_Committer_loc_count[project_for_current_commit][committer_for_current_commit] = \
                self.project_Committer_loc_count[project_for_current_commit][
                    committer_for_current_commit] + loc_count_for_current_commit

            self.project_Committer_total_file_list[project_for_current_commit][committer_for_current_commit] = \
                self.project_Committer_total_file_list[project_for_current_commit][
                    committer_for_current_commit] + files_for_current_commit
            self.project_Author_total_file_list[project_for_current_commit][author_for_current_commit] = \
                self.project_Author_total_file_list[project_for_current_commit][
                    author_for_current_commit] + files_for_current_commit

        for project in self.set_of_projects:
            for author in self.set_of_authors:
                self.project_Author_total_file_count[project][author] = len(
                    self.project_Author_total_file_list[project][author])
                self.project_Author_unique_file_count[project][author] = len(
                    list(dict.fromkeys(self.project_Author_total_file_list[project][author])))
        for project in self.set_of_projects:
            for committer in self.set_of_committers:
                self.project_Committer_total_file_count[project][committer] = len(
                    self.project_Committer_total_file_list[project][committer])
                self.project_Committer_unique_file_count[project][committer] = len(
                    list(dict.fromkeys(self.project_Committer_total_file_list[project][committer])))

    def remove_redundant_authors_and_committers_from_project_author_and_committer_lOC_and_file_count_dictionary(self):
        for project in list(self.project_Author_loc_count.keys()):
            for author in list(self.project_Author_loc_count[project]):
                if author not in self.project_set_of_authors[project]:
                    del (self.project_Author_loc_count[project][author])
        for project in list(self.project_Committer_loc_count.keys()):
            for committer in list(self.project_Committer_loc_count[project]):
                if committer not in self.project_set_of_committers[project]:
                    del (self.project_Committer_loc_count[project][committer])
        # for Total files
        for project in list(self.project_Author_total_file_count.keys()):

            for author in list(self.project_Author_total_file_count[project]):
                if author not in self.project_set_of_authors[project]:
                    del (self.project_Author_total_file_count[project][author])
        for project in list(self.project_Committer_total_file_count.keys()):
            for committer in list(self.project_Committer_total_file_count[project]):
                if committer not in self.project_set_of_committers[project]:
                    del (self.project_Committer_total_file_count[project][committer])
        # for unique files
        for project in list(self.project_Author_unique_file_count.keys()):
            for author in list(self.project_Author_unique_file_count[project]):
                if author not in self.project_set_of_authors[project]:
                    del (self.project_Author_unique_file_count[project][author])
        for project in list(self.project_Committer_unique_file_count.keys()):
            for committer in list(self.project_Committer_unique_file_count[project]):
                if committer not in self.project_set_of_committers[project]:
                    del (self.project_Committer_unique_file_count[project][committer])

    def build_commit_set_of_files_and_commit_lOC_count_dictionary(self):
        for elem_list in self.commit_file_records:
            file = elem_list["file_id"]
            commit = elem_list["commit_id"]
            lines_added = elem_list["lines_added"]
            lines_deleted = elem_list["lines_deleted"]
            if commit not in self.commits_set_of_files:
                self.commits_set_of_files[commit] = list()
            self.commits_set_of_files[commit].append(file)
            if commit not in self.commits_loc_count:
                self.commits_loc_count[commit] = 0
            self.commits_loc_count[commit] = self.commits_loc_count[commit] + lines_added + lines_deleted

    def fill_project_committer_commit_count_and_project_author_commit_count(self):
        for elem_list in self.commit_records:
            project_name = elem_list["project_name_info"]["name"]
            author_id = self.BRID.reverse_identity_dict[elem_list["author_id"]]
            committer_id = self.BRID.reverse_identity_dict[elem_list["committer_id"]]

            if project_name not in self.project_author_commits_count.keys():
                self.project_author_commits_count[project_name] = dict()
            if author_id not in self.project_author_commits_count[project_name].keys():
                self.project_author_commits_count[project_name][author_id] = 1
            else:
                self.project_author_commits_count[project_name][author_id] = \
                    self.project_author_commits_count[project_name][
                        author_id] + 1
            if project_name not in self.project_committer_commits_count.keys():
                self.project_committer_commits_count[project_name] = dict()
            if committer_id not in self.project_committer_commits_count[project_name].keys():
                self.project_committer_commits_count[project_name][committer_id] = 1
            else:
                self.project_committer_commits_count[project_name][committer_id] = \
                    self.project_committer_commits_count[project_name][
                        committer_id] + 1

    def sorting_project_author_commit_etc_count_and_project_committer_commit_etc_count(self):
        for project in self.project_author_commits_count.keys():
            self.sorted_project_author_commits_count[project] = dict()
            self.sorted_project_author_commits_count[project] = dict(
                sorted(self.project_author_commits_count[project].items(),
                       key=lambda item: item[1], reverse=True))

        for project in self.project_committer_commits_count.keys():
            self.sorted_project_committer_commits_count[project] = dict()
            self.sorted_project_committer_commits_count[project] = dict(
                sorted(self.project_committer_commits_count[project].items(),
                       key=lambda item: item[1], reverse=True))
        for project in self.project_Author_loc_count.keys():
            self.sorted_project_author_loc_count[project] = dict()
            self.sorted_project_author_loc_count[project] = dict(
                sorted(self.project_Author_loc_count[project].items(),
                       key=lambda item: item[1], reverse=True))

        for project in self.project_Committer_loc_count.keys():
            self.sorted_project_committer_loc_count[project] = dict()
            self.sorted_project_committer_loc_count[project] = dict(
                sorted(self.project_Committer_loc_count[project].items(),
                       key=lambda item: item[1], reverse=True))
        for project in self.project_Author_total_file_count.keys():
            self.sorted_project_author_total_file_count[project] = dict()
            self.sorted_project_author_total_file_count[project] = dict(
                sorted(self.project_Author_total_file_count[project].items(),
                       key=lambda item: item[1], reverse=True))

        for project in self.project_Committer_total_file_count.keys():
            self.sorted_project_committer_total_file_count[project] = dict()
            self.sorted_project_committer_total_file_count[project] = dict(
                sorted(self.project_Committer_total_file_count[project].items(),
                       key=lambda item: item[1], reverse=True))
        for project in self.project_Author_unique_file_count.keys():
            self.sorted_project_author_unique_file_count[project] = dict()
            self.sorted_project_author_unique_file_count[project] = dict(
                sorted(self.project_Author_unique_file_count[project].items(),
                       key=lambda item: item[1], reverse=True))

        for project in self.project_Committer_unique_file_count.keys():
            self.sorted_project_committer_unique_file_count[project] = dict()
            self.sorted_project_committer_unique_file_count[project] = dict(
                sorted(self.project_Committer_unique_file_count[project].items(),
                       key=lambda item: item[1], reverse=True))

    def refined_project_unique_file_counts(self):
        project_set_of_files = dict()
        for p in self.set_of_projects:
            project_set_of_files[p] = set()

        for c in self.set_of_commits_file_action:
            p1 = self.commits_project_dictionary[c]
            project_set_of_files[p1] = project_set_of_files[p1].union(set(self.commits_set_of_files[c]))
        for p2 in self.set_of_projects:
            self.project_unique_file_count[p2] = len(project_set_of_files[p2])

    def test_function(self):
        for p in self.set_of_projects:
            total_loc_count_for_project = 0
            total_commit_count_for_project = 0
            total_file_count_for_project = 0
            for a in self.project_Committer_loc_count[p]:
                total_file_count_for_project = total_file_count_for_project + \
                                               self.project_Committer_total_file_count[p][a]
                total_commit_count_for_project = total_commit_count_for_project + \
                                                 self.project_committer_commits_count[p][
                                                     a]
                total_loc_count_for_project = total_loc_count_for_project + self.project_Committer_loc_count[p][a]
            if self.project_total_file_count[p] != total_file_count_for_project:
                print(f" total file count for project {p} do not match ")
            if self.project_total_loc_count[p] != total_loc_count_for_project:
                print(f" total loc count do not match for project {p}")

            if self.project_total_commits_count[p] != total_commit_count_for_project:
                print(f" total commits count do not match for project {p}")


if __name__ == "__main__":
    start_time = time.time()
    start_time_total = time.time()
    TH = TechnicalHeroes_data()
    end_time = time.time()
    total_time = end_time - start_time
    print("initialization done in {} seconds".format(total_time))
    start_time = time.time()
    TH.commit_author_committer_project_dictionary_set_of_commits_etc()
    end_time = time.time()
    total_time = end_time - start_time
    print(" first function done in {} seconds ".format(total_time))
    start_time = time.time()
    TH.build_project_list_of_commits_dictionary()
    end_time = time.time()
    total_time = end_time - start_time
    print(" second function done in {} seconds ".format(total_time))
    start_time = time.time()
    TH.build_commit_set_of_files_and_commit_lOC_count_dictionary()
    end_time = time.time()
    total_time = end_time - start_time
    print(" third function done  in {} seconds".format(total_time))
    start_time = time.time()
    TH.build_project_total_commit_lOC_and_file_count_dictionary()
    end_time = time.time()
    total_time = end_time - start_time
    print(" fourth  function done in {} seconds ".format(total_time))
    start_time = time.time()
    TH.build_project_author_and_committer_list_of_commits_dictionary()
    end_time = time.time()
    total_time = end_time - start_time
    print("fifth function done in {} seconds ".format(total_time))
    start_time = time.time()
    TH.fill_project_committer_commit_count_and_project_author_commit_count()
    end_time = time.time()
    total_time = end_time - start_time
    print("sixth function done in {} seconds ".format(total_time))
    start_time = time.time()
    TH.build_project_author_and_committer_lOC_and_file_count_dictionary_initialization()
    TH.build_project_author_and_committer_lOC_and_file_count_dictionary()
    end_time = time.time()
    total_time = end_time - start_time
    print("seventh function done in {} seconds ".format(total_time))
    start_time = time.time()
    TH.remove_redundant_authors_and_committers_from_project_author_and_committer_lOC_and_file_count_dictionary()
    end_time = time.time()
    total_time = end_time - start_time
    print("Eighth function done in {} seconds ".format(total_time))
    start_time = time.time()
    TH.sorting_project_author_commit_etc_count_and_project_committer_commit_etc_count()
    end_time = time.time()
    total_time = end_time - start_time
    print("Ninth function done in {} seconds ".format(total_time))
