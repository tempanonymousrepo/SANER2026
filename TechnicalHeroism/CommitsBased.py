from pymongo import MongoClient
from Build_reverse_identity_dictionary import Build_reverse_identity_dictionary
import time
import pickle as pkl


class TechnicalHeroes:
    def __init__(self):
        self.project_author_commits = dict()
        self.project_number_of_authors = dict()
        self.project_number_of_commits = dict()
        self.project_author_number_of_commits = dict()
        self.project_top_authors_commits = dict()
        self.heroproject_authors_commits = dict()
        self.project_hero_or_not = dict()
        self.BRID = Build_reverse_identity_dictionary()
        self.BRID.reading_identity_and_people_and_building_reverse_identity_dictionary()
        self.client = MongoClient("mongodb://localhost:27017/")  # Setting Up Connection with mongodb
        self.db = self.client['smartshark']  # Getting to the desired database
        self.file_name = self.db['commit_with_project_info']  # Getting to the desired table/document
        self.records = list(self.file_name.find({}))  # Extracting all the records

    def creating_project_author_commits(self):
        for elem in self.records:
            commit = elem['_id']
            author = elem['author_id']
            author_id = self.BRID.reverse_identity_dict[author]
            project = elem['project_name_info']['name']
            if project not in self.project_author_commits:
                self.project_author_commits[project] = dict()
            if author_id not in self.project_author_commits[project]:
                self.project_author_commits[project][author_id] = list()
            if commit not in self.project_author_commits[project][author_id]:
                self.project_author_commits[project][author_id].append(commit)
        file_path = 'project_author_commits.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.project_author_commits, file)
        print('completed')

    def loading_project_author_commits(self):
        file_path = 'project_author_commits.pkl'
        with open(file_path, 'rb') as file:
            self.project_author_commits = pkl.load(file)
        print('dictionary created')

    def extracting_project_number_of_authors(self):
        for project in self.project_author_commits:
            count = len(self.project_author_commits[project])
            self.project_number_of_authors[project] = count

    def extracting_project_number_of_commits(self):
        for project in self.project_author_commits:
            count = 0
            for author in self.project_author_commits[project]:
                count = count + len(self.project_author_commits[project][author])
            self.project_number_of_commits[project] = count

    def extracting_project_author_number_of_commits(self):
        for project in self.project_author_commits:
            if project not in self.project_author_number_of_commits:
                self.project_author_number_of_commits[project] = dict()
            for author in self.project_author_commits[project]:
                num = len(self.project_author_commits[project][author])
                self.project_author_number_of_commits[project][author] = num
        for project in self.project_author_number_of_commits:
            self.project_author_number_of_commits[project] = dict(sorted(self.project_author_number_of_commits[project].items(),key=lambda item: item[1], reverse=True))
        file_path = 'project_author_number_of_commits.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.project_author_number_of_commits, file)
        print('completed')

    def extracting_twenty_percent_authors(self):
        for project in self.project_author_number_of_commits:
            if project not in self.project_top_authors_commits:
                self.project_top_authors_commits[project] = dict()
            amount = int(0.2 * self.project_number_of_authors[project])
            counter = 0
            for author in self.project_author_number_of_commits[project]:
                if counter == amount:
                    break
                num = self.project_author_number_of_commits[project][author]
                self.project_top_authors_commits[project][author] = num
                counter = counter + 1

    def checking_hero_phenomenon(self):
        for project in self.project_top_authors_commits:
            counter = 0
            num = self.project_number_of_commits[project]
            for authors in self.project_top_authors_commits[project]:
                counter = counter + self.project_top_authors_commits[project][authors]
            if int(0.8*num) <= counter:
                self.project_hero_or_not[project] = 1
            else:
                self.project_hero_or_not[project] = 0

    def extracting_hero_projects_authors_commits(self):
        for project in self.project_top_authors_commits:
            if self.project_hero_or_not[project] == 1:
                if project not in self.heroproject_authors_commits:
                    self.heroproject_authors_commits[project] = dict()
                self.heroproject_authors_commits[project] = self.project_top_authors_commits[project]
        file_path = 'technicalHeroesCommits.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.heroproject_authors_commits, file)
        print('completed')


    def dumping_results_into_csv(self):
        csv_file = "technicalHeroesCommitsWise.csv"
        result_file = open(csv_file, "w")
        result_file.write("Hero_Project_Name")
        result_file.write(",")
        result_file.write("Hero Author Name")
        result_file.write(",")
        result_file.write("Commits")
        result_file.write(",")
        result_file.write("\n")
        for project in self.project_top_authors_commits:
            if self.project_hero_or_not[project] == 1:
                for authors in self.project_top_authors_commits[project]:
                    result_file.write(project)
                    result_file.write(",")
                    result_file.write(str(authors))
                    result_file.write(",")
                    result_file.write(str(self.project_top_authors_commits[project][authors]))
                    result_file.write('\n')
        file_path = 'hero_project_author_commits.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.project_top_authors_commits, file)
        print('completed')


if __name__ == "__main__":
    start_time = time.time()
    obj1 = TechnicalHeroes()
    obj1.creating_project_author_commits()
    obj1.loading_project_author_commits()
    obj1.extracting_project_number_of_authors()
    obj1.extracting_project_number_of_commits()
    obj1.extracting_project_author_number_of_commits()
    obj1.extracting_twenty_percent_authors()
    obj1.checking_hero_phenomenon()
    obj1.extracting_hero_projects_authors_commits()
    obj1.dumping_results_into_csv()
    end_time = time.time()
    total_time = end_time - start_time
    print(f" Total time taken to execute the code is  {total_time} seconds ")
