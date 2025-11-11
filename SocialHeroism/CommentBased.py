from pymongo import MongoClient
from Build_reverse_identity_dictionary import Build_reverse_identity_dictionary
import time
import pickle as pkl


class SocialHeroes:
    def __init__(self):
        self.project_author_comments = dict()
        self.project_number_of_authors = dict()
        self.project_number_of_comments = dict()
        self.project_author_number_of_comments = dict()
        self.project_top_author_comments = dict()
        self.project_hero_or_not = dict()
        self.heroproject_authors_comments = dict()
        self.BRID = Build_reverse_identity_dictionary()
        self.BRID.reading_identity_and_people_and_building_reverse_identity_dictionary()
        self.client = MongoClient("mongodb://localhost:27017/")  # Setting Up Connection with mongodb
        self.db = self.client['smartshark']  # Getting to the desired database
        self.file_name = self.db['comments_with_issue_and_project_info']  # Getting to the desired table/document
        self.records = list(self.file_name.find({}))  # Extracting all the records

    def creating_project_author_comments(self):
        for elem in self.records:
            comment = elem['_id']
            author = elem['author_id']
            author_id = self.BRID.reverse_identity_dict[author]
            project = elem['issue_info']['project_name_info']['name']
            if project not in self.project_author_comments:
                self.project_author_comments[project] = dict()
            if author_id not in self.project_author_comments[project]:
                self.project_author_comments[project][author_id] = list()
            if comment not in self.project_author_comments[project][author_id]:
                self.project_author_comments[project][author_id].append(comment)
        file_path = 'project_author_comments.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.project_author_comments, file)
        print('completed')

    def loading_project_author_comments(self):
        file_path = 'project_author_comments.pkl'
        with open(file_path, 'rb') as file:
            self.project_author_comments = pkl.load(file)
        print('dictionary created')

    def extracting_project_number_of_authors(self):
        for project in self.project_author_comments:
            count = len(self.project_author_comments[project])
            self.project_number_of_authors[project] = count

    def extracting_project_number_of_comments(self):
        for project in self.project_author_comments:
            count = 0
            for author in self.project_author_comments[project]:
                count = count + len(self.project_author_comments[project][author])
            self.project_number_of_comments[project] = count

    def extracting_project_author_number_of_comments(self):
        for project in self.project_author_comments:
            if project not in self.project_author_number_of_comments:
                self.project_author_number_of_comments[project] = dict()
            for author in self.project_author_comments[project]:
                num = len(self.project_author_comments[project][author])
                self.project_author_number_of_comments[project][author] = num
        for project in self.project_author_number_of_comments:
            self.project_author_number_of_comments[project] = dict(sorted(self.project_author_number_of_comments[project].items(), key=lambda item: item[1], reverse=True))
        file_path = 'project_author_number_of_comments.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.project_author_number_of_comments, file)
        print('completed')

    def extracting_twenty_percent_authors(self):
        for project in self.project_author_number_of_comments:
            if project not in self.project_top_author_comments:
                self.project_top_author_comments[project] = dict()
            amount = int(0.2 * self.project_number_of_authors[project])
            counter = 0
            for author in self.project_author_number_of_comments[project]:
                if counter == amount:
                    break
                num = self.project_author_number_of_comments[project][author]
                self.project_top_author_comments[project][author] = num
                counter = counter + 1

    def checking_hero_phenomenon(self):
        for project in self.project_top_author_comments:
            counter = 0
            num = self.project_number_of_comments[project]
            for authors in self.project_top_author_comments[project]:
                counter = counter + self.project_top_author_comments[project][authors]
            if int(0.8*num) <= counter:
                self.project_hero_or_not[project] = 1
            else:
                self.project_hero_or_not[project] = 0

    def extracting_hero_projects_authors_comments(self):
        for project in self.project_top_author_comments:
            if self.project_hero_or_not[project] == 1:
                if project not in self.heroproject_authors_comments:
                    self.heroproject_authors_comments[project] = dict()
                self.heroproject_authors_comments[project] = self.project_top_author_comments[project]
        file_path = 'technicalHeroesComments.pkl'
        with open(file_path, 'wb') as file:
            pkl.dump(self.heroproject_authors_comments, file)
        print('completed')

    def dumping_results_into_csv(self):
        csv_file = "technicalHeroesCommentsWise.csv"
        result_file = open(csv_file, "w")
        result_file.write("Hero_Project_Name")
        result_file.write(",")
        result_file.write("Hero Author Name")
        result_file.write(",")
        result_file.write("Commits")
        result_file.write(",")
        result_file.write("\n")
        for project in self.project_top_author_comments:
            if self.project_hero_or_not[project] == 1:
                for authors in self.project_top_author_comments[project]:
                    result_file.write(project)
                    result_file.write(",")
                    result_file.write(str(authors))
                    result_file.write(",")
                    result_file.write(str(self.project_top_author_comments[project][authors]))
                    result_file.write('\n')



if __name__ == "__main__":
    start_time = time.time()
    obj1 = SocialHeroes()
    obj1.creating_project_author_comments()
    obj1.loading_project_author_comments()
    obj1.extracting_project_number_of_comments()
    obj1.extracting_project_number_of_authors()
    obj1.extracting_project_author_number_of_comments()
    obj1.extracting_twenty_percent_authors()
    obj1.checking_hero_phenomenon()
    obj1.extracting_hero_projects_authors_comments()
    obj1.dumping_results_into_csv()
    end_time = time.time()
    total_time = end_time - start_time
    print(f" Total time taken to execute the code is  {total_time} seconds ")
