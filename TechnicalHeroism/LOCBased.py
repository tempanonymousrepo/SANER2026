from pymongo import MongoClient
from Build_reverse_identity_dictionary import Build_reverse_identity_dictionary
import time
import pickle as pkl


class TechnicalHeroesLOCBased:
    def __init__(self):
        self.commit_LOC = dict()
        self.commit_author = dict()
        self.file_id_commits = dict()
        self.project_src_files = dict()
        self.project_commit_LOC = dict()
        self.project_number_of_authors = dict()
        self.project_loc = dict()
        self.project_author_loc = dict()
        self.project_top_authors_loc = dict()
        self.project_hero_or_not_loc = dict()
        self.heroproject_authors_loc = dict()
        self.BRID = Build_reverse_identity_dictionary()
        self.BRID.reading_identity_and_people_and_building_reverse_identity_dictionary()
        self.client = MongoClient("mongodb://localhost:27017/")  # Setting Up Connection with mongodb
        self.db = self.client['smartshark']  # Getting to the desired database
        self.file_name = self.db['commit_with_project_info']  # Getting to the desired table/document
        self.records = list(self.file_name.find({}))  # Extracting all the records

    def extracting_commit_LOC(self):
        for elem in self.records:
            file_id = elem['file_id']
            commit = elem['commit_id']
            lines_added = elem['lines_added']
            lines_deleted = elem['lines_deleted']
            total_lines = int(lines_added) + int(lines_deleted)
            if commit not in self.commit_LOC:
                self.commit_LOC[commit] = total_lines
            else:
                self.commit_LOC[commit] = self.commit_LOC[commit] + total_lines
            if file_id not in self.file_id_commits:
                self.file_id_commits[file_id] = list()
            if commit not in self.file_id_commits[file_id]:
                self.file_id_commits[file_id].append(commit)
        file_path = 'commit_loc.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.commit_LOC, file)
        print('completed pickle 1')
        file_path = 'fileID_commits.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.file_id_commits, file)
        print('completed pickle 2')

    def extracting_commit_author(self):
        for elem in self.records:
            commit = elem['_id']
            author = elem['author_id']
            author_id = self.BRID.reverse_identity_dict[author]
            self.commit_author[commit] = author_id
        file_path = 'commit_author.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.commit_author, file)

    def extracting_project_src_files(self):
        file_path = 'project_src_files.pkl'
        with open(file_path, 'rb') as file:
            self.project_src_files = pkl.load(file)
        file_path = 'commit_loc.pkl'
        with open(file_path, 'rb') as file:
            self.commit_LOC = pkl.load(file)
        file_path = 'fileID_commits.pkl'
        with open(file_path, 'rb') as file:
            self.file_id_commits = pkl.load(file)
        file_path = 'fileID_commits.pkl'
        with open(file_path, 'rb') as file:
            self.file_id_commits = pkl.load(file)
        file_path = 'commit_author.pkl'
        with open(file_path, 'rb') as file:
            self.commit_author = pkl.load(file)

    def extracting_project_commit_LOC(self):
        for project in self.project_src_files:
            if project not in self.project_commit_LOC:
                self.project_commit_LOC[project] = dict()
            for file in self.project_src_files[project]:
                for commit in self.file_id_commits[file]:
                    lOC = self.commit_LOC[commit]
                    self.project_commit_LOC[project][commit] = lOC

    def extracting_project_author_LOC(self):
        for project in self.project_commit_LOC:
            if project not in self.project_author_loc:
                self.project_author_loc[project] = dict()
            for commit in self.project_commit_LOC[project]:
                author = self.commit_author[commit]
                loc = self.project_commit_LOC[project][commit]
                self.project_author_loc[project][author] = loc
        for project, authors in self.project_author_loc.items():
            # Get a list of authors with 0 commits
            authors_to_remove = [author for author, commits in authors.items() if commits == 0]
            # Remove authors with 0 commits
            for author in authors_to_remove:
                del self.project_author_loc[project][author]
        for project in self.project_author_loc:
            self.project_author_loc[project] = dict(sorted(self.project_author_loc[project].items(), key=lambda item: item[1], reverse=True))
        file_path = 'project_author_number_of_loc.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.project_author_loc, file)

    def extracting_project_number_of_authors(self):
        for project in self.project_author_loc:
            number = len(self.project_author_loc[project])
            self.project_number_of_authors[project] = number

    def extracting_project_loc(self):
        for project in self.project_author_loc:
            counter = 0
            if project not in self.project_loc:
                self.project_loc[project] = dict()
            for author in self.project_author_loc[project]:
                counter = counter + self.project_author_loc[project][author]
            self.project_loc[project] = counter

    def extracting_twenty_percent_authors(self):
        for project in self.project_author_loc:
            if project not in self.project_top_authors_loc:
                self.project_top_authors_loc[project] = dict()
            amount = int(0.2 * self.project_number_of_authors[project])
            counter = 0
            for author in self.project_author_loc[project]:
                if counter == amount:
                    break
                num = self.project_author_loc[project][author]
                self.project_top_authors_loc[project][author] = num
                counter = counter + 1

    def checking_hero_phenomenon(self):
        for project in self.project_top_authors_loc:
            counter = 0
            num = self.project_loc[project]
            for authors in self.project_top_authors_loc[project]:
                counter = counter + self.project_top_authors_loc[project][authors]
            if int(0.8*num) <= counter:
                self.project_hero_or_not_loc[project] = 1
            else:
                self.project_hero_or_not_loc[project] = 0

    def extracting_hero_projects_authors_commits(self):
        for project in self.project_top_authors_loc:
            if self.project_hero_or_not_loc[project] == 1:
                if project not in self.heroproject_authors_loc:
                    self.heroproject_authors_loc[project] = dict()
                self.heroproject_authors_loc[project] = self.project_top_authors_loc[project]
        file_path = 'technicalHeroesLOC.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.heroproject_authors_loc, file)

    def dumping_results_into_csv(self):
        csv_file = "technicalHeroesLOCWise.csv"
        result_file = open(csv_file, "w")
        result_file.write("Hero_Project_Name")
        result_file.write(",")
        result_file.write("Hero Author Name")
        result_file.write(",")
        result_file.write("Commits")
        result_file.write(",")
        result_file.write("\n")
        for project in self.project_top_authors_loc:
            if self.project_hero_or_not_loc[project] == 1:
                for authors in self.project_top_authors_loc[project]:
                    result_file.write(project)
                    result_file.write(",")
                    result_file.write(str(authors))
                    result_file.write(",")
                    result_file.write(str(self.project_top_authors_loc[project][authors]))
                    result_file.write('\n')


if __name__ == "__main__":
    start_time = time.time()
    obj1 = TechnicalHeroesLOCBased()
    obj1.extracting_commit_LOC()
    obj1.extracting_commit_author()
    obj1.extracting_project_src_files()
    obj1.extracting_project_commit_LOC()
    obj1.extracting_project_author_LOC()
    obj1.extracting_project_loc()
    obj1.extracting_project_number_of_authors()
    obj1.extracting_twenty_percent_authors()
    obj1.checking_hero_phenomenon()
    obj1.extracting_hero_projects_authors_commits()
    obj1.dumping_results_into_csv()
    end_time = time.time()
    total_time = end_time - start_time
    print(f" Total time taken to execute the code is  {total_time} seconds ")
