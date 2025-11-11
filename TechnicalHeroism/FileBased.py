from pymongo import MongoClient
from Build_reverse_identity_dictionary import Build_reverse_identity_dictionary
import time
import pickle as pkl


class TechnicalHeroesFileBased:
    def __init__(self):
        self.project_authors = dict()
        self.commit_author = dict()
        self.project_author_commits = dict()
        self.file_id_commits = dict()
        self.project_src_files = dict()
        self.project_author_file_id = dict()
        self.project_author_number_of_files = dict()
        self.project_number_of_authors = dict()
        self.project_number_of_files = dict()
        self.project_top_authors_files = dict()
        self.project_hero_or_not = dict()
        self.heroproject_authors_files = dict()
        self.BRID = Build_reverse_identity_dictionary()
        self.BRID.reading_identity_and_people_and_building_reverse_identity_dictionary()
        self.client = MongoClient("mongodb://localhost:27017/")  # Setting Up Connection with mongodb
        self.db = self.client['smartshark']  # Getting to the desired database
        self.file_name = self.db['file_action']  # Getting to the desired table/document
        self.records = list(self.file_name.find({}))  # Extracting all the records

    def extracting_project_authors(self):
        file_path = 'project_author_commits.pkl'
        with open(file_path, 'rb') as file:
            self.project_author_commits = pkl.load(file)
        for project in self.project_author_commits:
            if project not in self.project_authors:
                self.project_authors[project] = list()
            for authors in self.project_author_commits[project]:
                self.project_authors[project].append(authors)

    def extracting_commit_author(self):
        file_path = 'commit_author.pkl'
        with open(file_path, 'rb') as file:
            self.commit_author = pkl.load(file)
        file_path = 'project_src_files.pkl'
        with open(file_path, 'rb') as file:
            self.project_src_files = pkl.load(file)
        file_path = 'fileID_commits.pkl'
        with open(file_path, 'rb') as file:
            self.file_id_commits = pkl.load(file)

    def extracting_project_author_file_id(self):
        for project in self.project_src_files:
            if project not in self.project_author_file_id:
                self.project_author_file_id[project] = dict()
            for file in self.project_src_files[project]:
                for commit in self.file_id_commits[file]:
                    author = self.commit_author[commit]
                    if author not in self.project_author_file_id[project]:
                        self.project_author_file_id[project][author] = set()
                    self.project_author_file_id[project][author].add(file)

    def extracting_project_author_number_of_files(self):
        for project in self.project_author_file_id:
            if project not in self.project_author_number_of_files:
                self.project_author_number_of_files[project] = dict()
            for author in self.project_author_file_id[project]:
                num = len(self.project_author_file_id[project][author])
                self.project_author_number_of_files[project][author] = num
        for project in self.project_author_number_of_files:
            self.project_author_number_of_files[project] = dict(sorted(self.project_author_number_of_files[project].items(),key=lambda item: item[1], reverse=True))
        file_path = 'project_author_number_of_files.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.project_author_number_of_files, file)
        print('completed')

    def extracting_project_number_of_authors(self):
        for project in self.project_author_number_of_files:
            number = len(self.project_author_number_of_files[project])
            self.project_number_of_authors[project] = number

    def extracting_project_number_of_files(self):
        for project in self.project_author_number_of_files:
            count = 0
            for author in self.project_author_number_of_files[project]:
                count = count + self.project_author_number_of_files[project][author]
            self.project_number_of_files[project] = count

    def extracting_twenty_percent_authors(self):
        for project in self.project_author_number_of_files:
            if project not in self.project_top_authors_files:
                self.project_top_authors_files[project] = dict()
            amount = int(0.2 * self.project_number_of_authors[project])
            counter = 0
            for author in self.project_author_number_of_files[project]:
                if counter == amount:
                    break
                num = self.project_author_number_of_files[project][author]
                self.project_top_authors_files[project][author] = num
                counter = counter + 1

    def checking_hero_phenomenon(self):
        for project in self.project_top_authors_files:
            counter = 0
            num = self.project_number_of_files[project]
            for authors in self.project_top_authors_files[project]:
                counter = counter + self.project_top_authors_files[project][authors]
            if int(0.8*num) <= counter:
                self.project_hero_or_not[project] = 1
            else:
                self.project_hero_or_not[project] = 0

    def extracting_hero_projects_authors_commits(self):
        for project in self.project_top_authors_files:
            if self.project_hero_or_not[project] == 1:
                if project not in self.heroproject_authors_files:
                    self.heroproject_authors_files[project] = dict()
                self.heroproject_authors_files[project] = self.project_top_authors_files[project]
        file_path = 'technicalHeroesFiles.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.heroproject_authors_files, file)
        print('completed')

    def dumping_results_into_csv(self):
        csv_file = "technicalHeroesFileWise.csv"
        result_file = open(csv_file, "w")
        result_file.write("Hero_Project_Name")
        result_file.write(",")
        result_file.write("Hero Author Name")
        result_file.write(",")
        result_file.write("Commits")
        result_file.write(",")
        result_file.write("\n")
        for project in self.project_top_authors_files:
            if self.project_hero_or_not[project] == 1:
                for authors in self.project_top_authors_files[project]:
                    result_file.write(project)
                    result_file.write(",")
                    result_file.write(str(authors))
                    result_file.write(",")
                    result_file.write(str(self.project_top_authors_files[project][authors]))
                    result_file.write('\n')




if __name__ == "__main__":
    start_time = time.time()
    obj1 = TechnicalHeroesFileBased()
    obj1.extracting_commit_author()
    obj1.extracting_project_authors()
    obj1.extracting_project_author_file_id()
    obj1.extracting_project_author_number_of_files()
    obj1.extracting_project_number_of_authors()
    obj1.extracting_project_number_of_files()
    obj1.extracting_twenty_percent_authors()
    obj1.checking_hero_phenomenon()
    obj1.extracting_hero_projects_authors_commits()
    # obj1.dumping_results_into_csv()
    end_time = time.time()
    total_time = end_time - start_time
    print(f" Total time taken to execute the code is  {total_time} seconds ")
